from unittest.mock import patch
from nose.tools import ok_, eq_, raises

from moncli import MondayClient, entities as en
from moncli.api_v2 import constants
from moncli.enums import BoardKind, NotificationTargetType, WorkspaceKind

USERNAME = 'test.user@foobar.org' 
GET_ME_RETURN_VALUE = en.User(**{'creds': None, 'id': '1', 'email': USERNAME})

@patch.object(MondayClient, 'get_me')
@raises(en.client.AuthorizationError)
def test_should_fail_monday_client_authorization(get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE

    # Act
    MondayClient('not.my.username@whatever.gov', '', '')


@patch.object(MondayClient, 'get_me')
def test_should_create_monday_client(get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE

    # Act
    client = MondayClient(USERNAME, '', '')

    # Assert
    ok_(client != None)


@patch('moncli.api_v2.create_board')
@patch.object(MondayClient, 'get_me')
def test_should_create_a_new_board(get_me, create_board):

    # Arrange
    board_name = 'New Board 1'
    board_kind = BoardKind.private
    get_me.return_value = GET_ME_RETURN_VALUE
    create_board.return_value = {'id': '1', 'name': board_name, 'board_kind': board_kind.name}
    client = MondayClient(USERNAME, '', '')

    # Act
    board = client.create_board(board_name, board_kind)

    # Assert 
    ok_(board != None)
    eq_(board.name, board_name)
    eq_(board.board_kind, board_kind.name)


@patch('moncli.api_v2.get_boards')
@patch.object(MondayClient, 'get_me')
def test_should_retrieve_a_list_of_boards(get_me, get_boards):

    # Arrange
    test_boards = [{'id': '1', 'name': 'Board 1'}]
    get_me.return_value = GET_ME_RETURN_VALUE
    get_boards.return_value = test_boards
    client = MondayClient(USERNAME, '', '')

    # Act
    boards = client.get_boards()

    # Assert
    ok_(boards != None)
    eq_(len(boards), 1)
    eq_(boards[0].id, test_boards[0]['id'])
    eq_(boards[0].name, test_boards[0]['name'])


@patch.object(MondayClient, 'get_me')
@raises(en.client.NotEnoughGetBoardParameters)
def test_should_fail_to_retrieve_single_board_due_to_too_few_parameters(get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    client = MondayClient(USERNAME, '', '')

    # Act
    client.get_board()


@patch.object(MondayClient, 'get_me')
@raises(en.client.TooManyGetBoardParameters)
def test_should_fail_to_retrieve_single_board_due_to_too_many_parameters(get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    client = MondayClient(USERNAME, '', '')

    # Act
    client.get_board(id='1', name='Test Board 1')


@patch('moncli.api_v2.get_boards')
@patch.object(MondayClient, 'get_me')
def test_should_retrieve_a_board_by_id(get_me, get_boards):

    # Arrange 
    id = '1'
    name = 'Test Board 1'
    get_me.return_value = GET_ME_RETURN_VALUE
    get_boards.return_value = [{'id': id, 'name': name}]
    client = MondayClient(USERNAME, '', '')
    
    # Act
    board = client.get_board(id=id)

    # Assert
    ok_(board != None)
    eq_(board.id, id)
    eq_(board.name, name)


@patch('moncli.api_v2.get_boards')
@patch.object(MondayClient, 'get_board_by_id')
@patch.object(MondayClient, 'get_me')
def test_should_retrieve_a_board_by_name(get_me, get_board_by_id, get_boards):

    # Arrange 
    id = '2'
    name = 'Test Board 2'
    get_me.return_value = GET_ME_RETURN_VALUE
    get_boards.return_value = [{'id': '1', 'name': 'Test Board 1'}, {'id': id, 'name': name}]
    get_board_by_id.return_value = en.Board(creds={}, id=id, name=name)
    client = MondayClient(USERNAME, '', '')

    # Act 
    board = client.get_board(name=name)

    # Assert
    ok_(board != None)
    eq_(board.id, id)
    eq_(board.name, name)


@patch('moncli.api_v2.archive_board')
@patch.object(MondayClient, 'get_me')
def test_should_archive_a_board(get_me, archive_board):

    # Arrange 
    id = '1'
    get_me.return_value = GET_ME_RETURN_VALUE
    archive_board.return_value = {'id': id}
    client = MondayClient(USERNAME, '', '')

    # Act 
    board = client.archive_board(id)

    # Assert
    ok_(board != None)
    eq_(board.id, id)


@patch.object(MondayClient, 'get_me')
@raises(en.client.AssetIdsRequired)
def test_should_fail_to_retrieve_assets_with_no_ids(get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    client = MondayClient(USERNAME, '', '')

    # Act
    client.get_assets([])


@patch('moncli.api_v2.get_assets')
@patch.object(MondayClient, 'get_me')
def test_should_retrieve_assets(get_me, get_assets):

    # Arrange
    asset_id = '12345'
    name = '33.jpg'
    url = 'http://test.monday.com/files/33.jpg'
    get_me.return_value = GET_ME_RETURN_VALUE
    get_assets.return_value = [{'id': asset_id, 'name': name, 'url': url}]

    client = MondayClient(USERNAME, '', '')
    
    # Act
    assets = client.get_assets([12345])

    # Assert
    ok_(assets)
    eq_(assets[0].id, asset_id)
    eq_(assets[0].name, name)
    eq_(assets[0].url, url)


@patch('moncli.api_v2.get_items')
@patch.object(MondayClient, 'get_me')
def test_should_get_items(get_me, get_items):

    # Arrange 
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 1'}]
    client = MondayClient(USERNAME, '', '')

    # Act 
    items = client.get_items()

    # Assert
    ok_(items != None)
    ok_(len(items), 1)


@patch('moncli.api_v2.get_updates')
@patch.object(MondayClient, 'get_me')
def test_should_get_updates(get_me, get_updates):

    # Arrange 
    id = '1'
    body = 'Hello, world!'
    get_me.return_value = GET_ME_RETURN_VALUE
    get_updates.return_value = [{'id': id, 'body': body}]
    client = MondayClient(USERNAME, '', '')

    # Act 
    updates = client.get_updates()

    # Assert
    ok_(updates != None)
    ok_(len(updates), 1)
    eq_(updates[0].id, id)
    eq_(updates[0].body, body)


@patch('moncli.api_v2.clear_item_updates')
@patch.object(MondayClient, 'get_me')
def test_should_clear_item_updates(get_me, clear_item_updates):

    # Arrange 
    id = '1'
    name = 'Hello, world!'
    get_me.return_value = GET_ME_RETURN_VALUE
    clear_item_updates.return_value = {'id': id, 'name': name}
    client = MondayClient(USERNAME, '', '')

    # Act 
    item = client.clear_item_updates(id)

    # Assert
    ok_(item)
    eq_(item.id, id)
    eq_(item.name, name)


@patch('moncli.api_v2.delete_update')
@patch.object(MondayClient, 'get_me')
def test_should_delete_update(get_me, delete_update):

    # Arrange 
    id = '1'
    item_id = '1'
    creator_id = GET_ME_RETURN_VALUE.id
    get_me.return_value = GET_ME_RETURN_VALUE
    delete_update.return_value = {'id': id, 'item_id': item_id, 'creator_id': creator_id}
    client = MondayClient(USERNAME, '', '')

    # Act 
    update = client.delete_update(id)

    # Assert
    ok_(update)
    eq_(update.id, id)
    eq_(update.item_id, item_id)
    eq_(update.creator_id, creator_id)


@patch('moncli.api_v2.create_notification')
@patch.object(MondayClient, 'get_me')
def test_should_create_a_notification(get_me, create_notification):

    # Arrange 
    text = 'Text 1'
    get_me.return_value = GET_ME_RETURN_VALUE
    create_notification.return_value = {'id': '1', 'text': text}
    client = MondayClient(USERNAME, '', '')

    # Act 
    notification = client.create_notification(text, '1', '2', NotificationTargetType.Post)

    # Assert
    ok_(notification != None)
    ok_(notification.text, text)


@patch('moncli.api_v2.create_or_get_tag')
@patch.object(MondayClient, 'get_me')
def test_should_create_or_get_a_tag(get_me, create_or_get_tag):

    # Arrange 
    name = 'Tag 1'
    get_me.return_value = GET_ME_RETURN_VALUE
    create_or_get_tag.return_value = {'id': '1', 'name': name, 'color': 'Black'}
    client = MondayClient(USERNAME, '', '')

    # Act 
    tag = client.create_or_get_tag(name)

    # Assert
    ok_(tag != None)
    eq_(tag.name, name)


@patch('moncli.api_v2.get_tags')
@patch.object(MondayClient, 'get_me')
def test_should_retrieve_list_of_tags(get_me, get_tags):

    # Arrange 
    name = 'Tag 1'
    get_me.return_value = GET_ME_RETURN_VALUE
    get_tags.return_value = [{'id': '1', 'name': name, 'color': 'Black'}]
    client = MondayClient(USERNAME, '', '')

    # Act 
    tags = client.get_tags()

    # Assert
    ok_(tags != None)
    eq_(len(tags), 1)
    eq_(tags[0].name, name)

@patch('moncli.api_v2.create_workspace')
@patch.object(MondayClient, 'get_me')
def test_should_create_workspace(get_me, create_workspace):

    # Arrange
    id = '12345'
    name = 'Workspace'
    kind = WorkspaceKind.open
    description = 'This is a test workspace.'
    get_me.return_value = GET_ME_RETURN_VALUE
    create_workspace.return_value = {'id': id, 'name': name, 'kind': kind.name, 'description': description}
    client = MondayClient(USERNAME, '', '')

    # Act
    workspace = client.create_workspace(name, kind, description=description)

    # Assert
    ok_(workspace != None)
    eq_(workspace.id, id)
    eq_(workspace.name, name)
    eq_(workspace.kind, kind.name)
    eq_(workspace.description, description)


@patch('moncli.api_v2.get_users')
@patch.object(MondayClient, 'get_me')
def test_should_retrieve_list_of_users(get_me, get_users):

    # Arrange 
    name = 'User 1'
    email = 'user.one@test.com'
    get_me.return_value = GET_ME_RETURN_VALUE
    get_users.return_value = [{'id': '1', 'name': name, 'email': email}]
    client = MondayClient(USERNAME, '', '')

    # Act 
    users = client.get_users()

    # Assert
    ok_(users != None)
    eq_(len(users), 1)
    eq_(users[0].name, name)
    eq_(users[0].email, email)


@patch('moncli.api_v2.get_teams')
@patch.object(MondayClient, 'get_me')
def test_should_retrieve_list_of_teams(get_me, get_teams):

    # Arrange 
    name = 'User 1'
    get_me.return_value = GET_ME_RETURN_VALUE
    get_teams.return_value = [{'id': '1', 'name': name}]
    client = MondayClient(USERNAME, '', '')

    # Act 
    teams = client.get_teams()

    # Assert
    ok_(teams != None)
    eq_(len(teams), 1)
    eq_(teams[0].name, name)


@patch('moncli.api_v2.get_me')
@patch.object(MondayClient, 'get_me')
def test_should_retrieve_me(get_me, get_me_client):

    # Arrange 
    name = 'User 2'
    get_me.return_value = GET_ME_RETURN_VALUE
    get_me_client.return_value = {'id': '1', 'name': name, 'email': USERNAME}
    client = MondayClient(USERNAME, '', '')

    # Act 
    user = client.get_me()

    # Assert
    ok_(user != None)
    eq_(user.email, USERNAME)