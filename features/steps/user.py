import json
from re import U
from xmlrpc import client
from behave import *
from application import USERS

global response

# -------------------- GET/username--------------------


@given("some users are in the system")
def step_impl(context):
    USERS.update({"jasonb": {"name": "Jason Bourne"}})


@when("I retrieve the customer 'jasonb'")
def step_impl(context):
    context.page = context.client.get("/users/jasonb")
    assert context.page


@then('I should get a "{status:d}" response')
def step_impl(context, status):
    assert context.page.status_code is status


@then("the following user details are returned")
def step_impl(context):
    assert "Jason Bourne" in context.page.text


# -------------------- GET --------------------


# Arrange
@given("at least two users are in the system, which are")
def step_impl(context):

    for row in context.table:

        key = row["key"]
        name_user = row["name"]

        if not (key in USERS and USERS[key]["name"] == name_user):
            USERS.update({key: {"name": name_user}})


# Act
@when("I request system users")
def step_impl(context):
    context.page = context.client.get("/users/")
    assert context.page


# Assert
@then("I should get following response")
def step_impl(context):
    data = json.loads(context.page.text)

    for row in context.table:
        assert row["key"] in data
        assert data[row["key"]]["name"] == row["name"]

    assert context.page.status_code == 200


# -------------------- POST --------------------


@given("user '{key}' isn't exist in the system")
def step_impl(context, key):
    assert not USERS.get(key)


@when('I add user "{user}" with name "{name_user}"')
def step_impl(context, user, name_user):
    # print(new_user)
    context.headers = {"content-type": "application/json"}
    context.url = "/users/"
    context.body = {user: {"name": name_user}}

    # context.response = requests.session().post(context.url, data=json.dumps(context.body), headers=context.headers)

    context.page = context.client.post(
        context.url, data=json.dumps(context.body), headers=context.headers
    )

    # context.client.get('/users/aylen')


# print(context.res.text)
# context.res = requests.post(url, data=json.dumps(new_user), headers=headers)


@then("I should insert correctly to user 'aylen'")
def step_impl(context):

    assert {"success": "true"} == json.loads(
        context.page.text
    ) and context.page.status_code == 201


# -------------------- PUT --------------------


@given("user with the following information exists in the system")
def step_impl(context):

    key = context.table[0]["key"]
    name = context.table[0]["name"]

    if not (key in USERS and name == USERS[key]["name"]):
        USERS.update({key: name})


@when('I update user "{key}" with new name "{user_name}"')
def step_impl(context, user_name, key):

    context.headers = {"content-type": "application/json"}
    context.url = f"/users/{key}"
    context.body = {"name": user_name}

    context.page = context.client.put(
        context.url, data=json.dumps(context.body), headers=context.headers
    )


@then("I should get following data")
def step_impl(context):
    name = context.table[0]["name"]
    response = json.loads(context.page.text)

    assert name == response and context.page.status_code == 200


""" @then(u'the following data is returned')
def step_impl(context):
    resquest = context.body
    response = json.loads(context.page.text)
    print(response)
    assert response['name'] == resquest['name'] """


# -------------------- DELETE --------------------


@when('I delete user "{key}"')
def step_impl(context, key):

    context.headers = {"content-type": "application/json"}
    context.url = f"/users/{key}"

    context.page = context.client.delete(context.url, headers=context.headers)


@then('I should delete correctly to user "brend"')
def step_impl(context):

    assert {"success": "true"} == json.loads(
        context.page.text
    ) and context.page.status_code == 200
