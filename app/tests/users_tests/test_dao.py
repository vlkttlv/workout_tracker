import pytest
from app.users.dao import UsersDAO

@pytest.mark.asyncio(scope="session")
@pytest.mark.parametrize("id,exists,email", [
    (1, True, 'vvb63@tpu.ru'),
    (2, True, 'test@test.ru'),
    (20, False, 'email@tpu.com')
])
async def test_find_user_by_id(id, exists, email):
    user = await UsersDAO.find_one_or_none(id=id)
    if exists:
        assert user
        assert user.email == email
        assert user.id == id
    else:
        assert not user