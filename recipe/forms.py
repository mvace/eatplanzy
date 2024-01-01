from django import forms
from .models import Comment, Recipe


class AddRecipeForm(forms.ModelForm):
    uploaded_image = forms.ImageField(
        label="Recipe Image",
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "custom-file-input"}),
    )

    name = forms.CharField(
        label="",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Recipe Name",
            }
        ),
    )

    description = forms.CharField(
        label="",
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Description",
                "rows": "4",
            }
        ),
    )

    ingredients = forms.CharField(
        label="Ingredients",
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Enter each ingredient on a separate line.",
                "rows": "4",
            }
        ),
    )

    steps = forms.CharField(
        label="Steps",
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Enter each step on a separate line.",
                "rows": "4",
            }
        ),
    )

    nutrients = forms.CharField(
        label="Nutrients per portion",
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Enter each nutirent with its value on a separate line.\n kcal: ..\n protein: ..\n carbs: ..\n ...",
                "rows": "4",
            }
        ),
    )
    serves = forms.IntegerField(
        label="Serves",
        required=True,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    dish_type = forms.CharField(
        label="Dish Type",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Dish Type",
                "maxlength": "30",
            }
        ),
    )

    class Meta:
        model = Recipe
        fields = [
            "name",
            "description",
            "uploaded_image",
            "ingredients",
            "steps",
            "nutrients",
            "serves",
            "maincategory",
            "subcategory",
            "dish_type",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["serves"].queryset = Recipe.objects.filter(serves__gt=0)

        self.generate_choice_field("maincategory", "Main Category")
        self.generate_choice_field("subcategory", "Sub Category")

        if self.instance.ingredients:
            self.initial["ingredients"] = "\n".join(self.instance.ingredients)
        if self.instance.steps:
            self.initial["steps"] = "\n".join(self.instance.steps)
        if self.instance.nutrients:
            self.initial["nutrients"] = "\n".join(self.instance.nutrients)

    def generate_choice_field(self, field_name, label):
        # Get the distinct values for the field from the Recipe model
        field_choices = Recipe.objects.values_list(field_name, flat=True).distinct()
        field_choices = [(choice, choice) for choice in field_choices]

        # Create the choice field
        self.fields[field_name] = forms.ChoiceField(
            label=label,
            required=True,
            choices=[("", f"Select a {field_name}")] + field_choices,
            widget=forms.Select(attrs={"class": "form-control"}),
        )


class CommentForm(forms.ModelForm):
    text = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Type your comment...",
                "size": "30",
                "maxlength": "255",
            }
        ),
    )

    class Meta:
        model = Comment
        fields = ["text"]
