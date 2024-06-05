



def test_login_page(test_client):

    response = test_client.get('/auth/login')
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Username' in response.data
    assert b'Password' in response.data


def test_valid_login_logout(test_client, init_database):
    response  = test_client.post('/auth/login', data=dict(
        username='first_user',
        password='password1'
    ), follow_redirects=True)
    assert response.status_code  ==  200
    assert b'Welcome, first_user' in response.data
    assert b'Logout' in response.data
    assert b'Login' not in response.data
    assert b'Register' not in response.data


    response = test_client.get('/auth/logout', follow_redirects=True)
    assert response.status_code  ==  200
    assert b'Login' in response.data
    assert b'Register' in response.data



def invalid_login(test_client):
    response  = test_client.post('/auth/login', data=dict(
       username='test',
       password='test213'
    ), follow_redirects=True)
    assert response.status_code   ==  200
    assert b'Login' in response.data
    assert b'Username' in response.data
    assert b'Password' in response.data



