



def test_login_page(test_client):

    response = test_client.get('/auth/login')
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Username' in response.data
    assert b'Password' in response.data


def test_valid_login_logout(test_client, init_database):
    response  = test_client.post('/auth/login', data={
        'username': 'first_user',
        'password': 'password1'
    }, follow_redirects=True)
    assert response.status_code  ==  200
    assert b'Welcome, first_user' in response.data
    assert b'Logout' in response.data
    assert b'Login' not in response.data
    assert b'Register' not in response.data


    response = test_client.get('/auth/logout', follow_redirects=True)
    assert response.status_code  ==  200
    assert b'Login' in response.data
    assert b'Register' in response.data



def test_invalid_login(test_client, init_database):
    response  = test_client.post('/auth/login', data={
       'username': 'test',
       'password': 'test213'
    }, follow_redirects=True)
    assert response.status_code   ==  200
    assert b'Login' in response.data
    assert b'Username' in response.data
    assert b'Password' in response.data


def test_login_already_logged_in(test_client, init_database, log_in_default_user):
    response  = test_client.get('/auth/login', data={'username': 'first_user', 'password': 'password1'}, follow_redirects=True)
    assert response.status_code   ==  200
    assert b'Welcome, first_user' in response.data
    assert b'Logout' in response.data
    assert b'Register' not in response.data


def test_valid_register(test_client, init_database):

    response  = test_client.post('/auth/register', data={
        'username': 'test_user',
        'email': 'test_user@test.com',
        'password': 'password1',
        'password2': 'password1'
    }, follow_redirects=True)
    assert response.status_code   ==  200
    assert b'Login' in response.data
    assert b'Register' not in response.data

    response = test_client.get('/auth/logout', follow_redirects=True)
    assert response.status_code     ==  200
    assert b'Login' in response.data
    assert b'Register' in response.data
    

    response = test_client.post('/auth/login', data={'username': 'test_user', 'password': 'password1'}, follow_redirects=True)
    assert response.status_code    ==  200
    assert b'Welcome, test_user' in response.data
    assert b'Logout' in response.data
    assert b'Login' not in response.data
    assert b'Register' not in response.data

    response = test_client.get('/auth/logout', follow_redirects=True)
    assert response.status_code     ==  200
    assert b'Login' in response.data
    assert b'Register' in response.data
    



def test_invalid_register(test_client, init_database):
    response   = test_client.post('/auth/register', data={
        'username':  'test',
        'email':  'test@test.com',
        'password':  'test213',
        'password2':  '213test'
    }, follow_redirects=True)
    assert response.status_code    ==  200
    assert b'Register' in response.data
    assert b'Email' in response.data
    assert b'Password' in response.data
    assert b'Repeat Password' in response.data
    assert b'Field must be equal to password.' in response.data



#TODO add more checks
def test_duplicate_register(test_client, init_database):
    response    = test_client.post('/auth/register', data={
        'username':   'test1',
        'email':   'test@test.com',
        'password':   'test213',
        'password2':   'test213',
    }, follow_redirects=True)
    assert response.status_code     ==  200
    assert b'Login' in response.data
    assert b'Username' in response.data
    assert b'Password' in response.data


    response = test_client.get('/auth/logout', follow_redirects=True)

    response    = test_client.post('/auth/register', data={
        'username':   'test1',
        'email':   'test@test.com',
        'password':   'test2134',
        'password2':   'test2134',
    }, follow_redirects=True)
    assert response.status_code     ==  200
    print(response.data)
    # assert b'Internal Server Error' in response.data
