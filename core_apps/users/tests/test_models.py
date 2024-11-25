from django.contrib.auth import get_user_model
import pytest
from django.utils.translation import gettext_lazy as _
from pytest_factoryboy import register
from core_apps.users.tests.factories import UserFactory
User = get_user_model()
register(UserFactory)

@pytest.mark.django_db
def test_create_normal_user(normal_user):
    assert normal_user.first_name is not None
    assert normal_user.last_name is not None
    assert normal_user.email is not None
    assert normal_user.password is not None
    assert normal_user.pkid is not None
    assert not normal_user.is_staff 
    assert not normal_user.is_superuser

@pytest.mark.django_db
def test_create_super_user(super_user):
    assert super_user.first_name is not None
    assert super_user.last_name is not None
    assert super_user.email is not None
    assert super_user.password is not None
    assert super_user.pkid is not None
    assert super_user.is_staff 
    assert super_user.is_superuser

@pytest.mark.django_db
def test_get_full_name_user(normal_user):
    # مقدار مورد انتظار
    expected_full_name = f"{normal_user.first_name} {normal_user.last_name}"
    
    # متد مورد آزمایش
    full_name = normal_user.get_full_name
    
    # خروجی‌ها برای دیباگ
    print("Expected:", expected_full_name)
    print("Actual:", full_name)
    
    # بررسی
    assert full_name == expected_full_name


@pytest.mark.django_db
def test_get_short_name(normal_user):
    short_name = normal_user.get_short_name()
    excepted_short_name = f"{normal_user.first_name}"
    assert short_name == excepted_short_name

@pytest.mark.django_db
def test_update_user(normal_user):
    new_first_name = "masi"
    new_last_name = "shayesteh"
    normal_user.first_name = new_first_name
    normal_user.last_name = new_last_name
    normal_user.save()

    assert normal_user.first_name == new_first_name
    assert normal_user.last_name == new_last_name

@pytest.mark.django_db
def test_delete_user(normal_user):
    pk_normal_user = normal_user.pk
    normal_user.delete()

    with pytest.raises(User.DoesNotExist):
        User.objects.get(pk=pk_normal_user)


@pytest.mark.django_db
def test_str_user(normal_user):
    assert str(normal_user) == f"{normal_user.email}"


@pytest.mark.django_db
def test_str_user(normal_user):
    assert str(normal_user) == f"{normal_user.email}"

@pytest.mark.django_db
def test_user_valid_email(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(email="mahsa.com")
    assert str(err.value) == "لطفا یک ایمیل معتبر وارد کنید"

@pytest.mark.django_db
def test_normal_user_is_email_normalized(normal_user):
    email = normal_user.email
    assert email == email.lower()

@pytest.mark.django_db
def test_super_user_is_email_normalized(super_user):
    
    email = super_user.email
    assert email == email.lower()

@pytest.mark.django_db
def test_create_user_with_no_firstname(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(first_name=None)
    assert str(err.value) == 'لطفا نام خود را وارد کنید'

@pytest.mark.django_db
def test_create_user_with_no_firstname(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(first_name=None)
    assert str(err.value) == 'لطفا نام خود را وارد کنید'

@pytest.mark.django_db
def test_create_user_with_no_last_name(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(last_name=None)
    assert str(err.value) == 'لطفا نام خانوادگی خود را وارد کنید'

@pytest.mark.django_db
def test_create_user_with_no_email(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(email=None)
    assert str(err.value) == 'لطفا ایمیل معتبر وارد کنید'

@pytest.mark.django_db
def test_create_user_with_no_email(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(email=None)
    assert str(err.value) == 'لطفا ایمیل معتبر وارد کنید'

