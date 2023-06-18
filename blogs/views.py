from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .forms import (
    SignUpForm,
    BlogsDetailsForm,
    CommentForm,
    BlogUpdateForm,
    CommentUpdateForm,
    UserUpdateForm,
    ProfileUpdateForm,
)
from .models import CustomUser, BlogsDetails, Comment
from django.urls import reverse_lazy
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


class SignupCreateView(CreateView):
    model = CustomUser
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    #add this in project urls.py for redirct Auth login Page 
    #path("accounts/", include("django.contrib.auth.urls")), 
    template_name = "signup.html"

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        date_of_birth = form.cleaned_data.get("date_of_birth")
        is_role = form.cleaned_data.get("is_role")
        values = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": date_of_birth,
            "is_role": is_role,
        }
        message = render_to_string("mail.html", {"context": values})
        send_mail(
            subject="New Mail",
            message=message,
            html_message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )
        return super().form_valid(form)


class CreateBlogsCreateView(CreateView):
    model = BlogsDetails
    form_class = BlogsDetailsForm
    success_url = reverse_lazy("blogs")
    template_name = "create_blog.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        self.object = form.save()
        reader_email = CustomUser.objects.filter(is_staff=True)
        id = BlogsDetails.objects.last()
        for email in reader_email:
            mail = email.email
            print(mail)
            send_mail(
                subject="New Mail",
                message="New Mail is Added  http://127.0.0.1:8000/blog/" + str(id.id),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[mail],
            )
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    success_url = reverse_lazy("blogs")
    template_name = "comment.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.blog_title = BlogsDetails.objects.get(id=self.kwargs["id"])
        # print(self.request.__dict__) # x=self.kwargs["id"]
        return super().form_valid(form)


class AddBlogsListView(ListView):
    model = BlogsDetails
    template_name = "home.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blogs"] = BlogsDetails.objects.all().order_by("-id")[:5]
        context["rendom_blogs"] = BlogsDetails.objects.all().order_by("?")[:3]
        return context


class BlogsListView(ListView):
    paginate_by = 5
    model = BlogsDetails
    template_name = "blogs_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogs = BlogsDetails.objects.all().order_by("-blog_date")

        paginator = Paginator(blogs, self.paginate_by)
        Page = self.request.GET.get("page")
        try:
            file_exams = paginator.page(Page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)

        context["blogs"] = file_exams
        return context


class BlogDetailsListView(ListView):
    model = BlogsDetails
    template_name = "blog_details.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get(self, request, **kwargs):
        object = BlogsDetails.objects.get(id=kwargs["id"])
        id = object.id
        blog = BlogsDetails.objects.filter(id=id)
        comment = Comment.objects.filter(blog_title=object).order_by("-id")
        context = {"blog": blog, "comment": comment}
        return render(request, "blog_details.html", context)


class BloggerDetailsListView(ListView):
    model = CustomUser
    template_name = "blogger_details.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get(self, request, **kwargs):
        object = CustomUser.objects.get(id=kwargs["id"])
        blogger = CustomUser.objects.filter(id=object.id)
        blogs = BlogsDetails.objects.filter(created_by=object).order_by("-blog_date")
        context = {"blogger": blogger, "blogs": blogs}
        return render(request, "blogger_details.html", context)


class BloggersListView(ListView):
    model = CustomUser
    template_name = "bloggers_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blogger"] = CustomUser.objects.filter(is_blogger=True).order_by(
            "first_name"
        )
        return context


class BlogUpdateView(UpdateView):
    model = BlogsDetails
    form_class = BlogUpdateForm
    template_name = "update_blog.html"
    success_url = reverse_lazy("blogs")


class BlogDeleteView(DeleteView):
    model = BlogsDetails
    template_name = "delete.html"
    success_url = reverse_lazy("blogs")

    def get(self, request, **kwargs):
        object = BlogsDetails.objects.get(id=kwargs["pk"])
        blog = BlogsDetails.objects.filter(id=object.id)
        context = {"blog": blog}
        return render(request, "delete_blog.html", context)


class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentUpdateForm
    template_name = "update_comment.html"
    success_url = reverse_lazy("blogs")


class CommentDeleteView(DeleteView):
    model = Comment
    template_name = "delete_comment.html"
    success_url = reverse_lazy("blogs")

    def get(self, request, **kwargs):
        object = Comment.objects.get(id=kwargs["pk"])
        comment = Comment.objects.filter(id=object.id)
        context = {"comment": comment}
        return render(request, "delete_comment.html", context)


class UserUpdateView(UpdateView):
    model = CustomUser
    form_class = UserUpdateForm
    template_name = "update_blogger.html"
    success_url = reverse_lazy("bloggers")


class UserDeleteView(DeleteView):
    model = CustomUser
    template_name = "delete_user.html"
    success_url = reverse_lazy("bloggers")

    def get(self, request, **kwargs):
        object = CustomUser.objects.get(id=kwargs["pk"])
        user = CustomUser.objects.filter(id=object.id)
        context = {"user": user}
        return render(request, "delete_blogger.html", context)


class ProfileUpdateForm(UpdateView):
    model = CustomUser
    form_class = ProfileUpdateForm
    template_name = "profile.html"
    success_url = reverse_lazy("home")
