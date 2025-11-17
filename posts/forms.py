from django import forms
from django.core.exceptions import ValidationError
from .models import Post


# ========== Form لإنشاء وتعديل البوست ==========
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # عدّل الحقول هنا حسب model حقك
        fields = ["title", "content", "image", "is_published"]
        # لو عندك حقل category في الـ model أضِفه:
        # fields = ["title", "content", "image", "category", "is_published"]

    def clean_title(self):
        title = self.cleaned_data["title"]
        banned = ["spam", "forbidden"]
        if any(b in title.lower() for b in banned):
            raise ValidationError("العنوان يحتوي كلمات ممنوعة.")
        return title


# ========== Form البحث والفِلترة ==========
class SearchForm(forms.Form):
    # كلمة البحث
    q = forms.CharField(
        label="كلمة البحث",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Title or content...",
            }
        ),
    )

    # نحاول نأخذ CATEGORY_CHOICES من الموديل، ولو مو موجودة نخليها فاضية
    _cat_choices = getattr(Post, "CATEGORY_CHOICES", [])
    category = forms.ChoiceField(
        label="التصنيف",
        required=False,
        choices=[("", "All")] + list(_cat_choices),
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    # هل هو منشور؟
    is_published = forms.NullBooleanField(
        label="منشور؟",
        required=False,
        widget=forms.NullBooleanSelect(attrs={"class": "form-select"}),
    )

    # ترتيب النتائج
    order = forms.ChoiceField(
        label="الترتيب",
        required=False,
        choices=[
            ("-published_at", "الأحدث أولًا"),
            ("published_at", "الأقدم أولًا"),
            ("title", "العنوان A→Z"),
            ("-title", "العنوان Z→A"),
        ],
        initial="-published_at",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    # عدد النتائج في الصفحة
    per_page = forms.IntegerField(
        label="عدد النتائج/صفحة",
        required=False,
        min_value=1,
        max_value=100,
        initial=10,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
