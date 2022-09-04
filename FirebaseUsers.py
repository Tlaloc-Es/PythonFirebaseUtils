# https://blog.icodes.tech/posts/python-firebase-authentication.html

import click
import requests

apikey = 'apikey'

DEFAULT_EMAIL = 'user@user.user'
DEFAULT_PASSWORD = 'password'


@click.group()
def cli1():
    pass


@cli1.command()
@click.option('--email', default=DEFAULT_EMAIL, help='Insert your email.')
@click.option('--password', default=DEFAULT_PASSWORD, prompt='Insert your password')
def new_user(email, password):
    """Create new firebase user"""
    details = {
        'email': email,
        'password': password,
        'returnSecureToken': True
    }
    # send post request
    r = requests.post(
        'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={}'.format(apikey), data=details)
    # check for errors in result
    if 'error' in r.json().keys():
        return {'status': 'error', 'message': r.json()['error']['message']}
    # if the registration succeeded
    if 'idToken' in r.json().keys():
        return {'status': 'success', 'idToken': r.json()['idToken']}


@click.group()
def cli2():
    pass


@cli2.command()
@click.option('--idToken', help='Insert your idToken.')
def verify_email(idToken):
    """Verify email"""
    headers = {
        'Content-Type': 'application/json',
    }
    data = '{"requestType":"VERIFY_EMAIL","idToken":"'+idToken+'"}'
    r = requests.post(
        'https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={}'.format(apikey), headers=headers, data=data)
    if 'error' in r.json().keys():
        return {'status': 'error', 'message': r.json()['error']['message']}
    if 'email' in r.json().keys():
        return {'status': 'success', 'email': r.json()['email']}


@click.group()
def cli3():
    pass


@cli3.command()
@click.option('--email', default=DEFAULT_EMAIL, help='Insert your email.')
@click.option('--password', default=DEFAULT_PASSWORD, prompt='Insert your password')
def sign_in(email, password):
    """Sing in a user inside firebase backend"""
    details = {
        'email': email,
        'password': password,
        'returnSecureToken': True
    }
    # Post request
    r = requests.post(
        'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={}'.format(apikey), data=details)
    # check for errors
    if 'error' in r.json().keys():
        data = {'status': 'error', 'message': r.json()['error']['message']}
        print(data)
        return data
    # success
    if 'idToken' in r.json().keys():
        data = {'status': 'success', 'idToken': r.json()['idToken']}
        print(data)
        return data


cli = click.CommandCollection(sources=[cli1, cli2, cli3])


if __name__ == '__main__':
    cli()
