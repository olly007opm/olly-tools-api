#  olly-tools-api | game.py
#  Last modified: 08/05/2022, 09:33
#  Copyright (c) 2022 Olly (https://olly.ml/). All rights reserved.

import datetime
from fastapi import APIRouter, Depends, Response, Request, Form
from auth_routes import auth

# Get the database
from firebase import get_database
db = get_database()

router = APIRouter(
    prefix="/game",
    tags=["game"],
)


@router.post("/xo/create", summary="Create a noughts and crosses game", tags=["noughts-and-crosses"])
def xo_create(response: Response, user=Depends(auth)):
    import random
    chars = "0123456789abcdef"
    code = ""
    for i in range(6):
        code += random.choice(chars)

    game_doc = db.collection('games').document()
    game_doc.set({
        'id': game_doc.id,
        'code': code,
        'type': 'xo',
        'status': 'waiting',
        'players': [user['id']],
        'board': ['-' for i in range(9)],
        'winner': None,
        'turn': 1,
        'turn_count': 0,
        'created_at': datetime.datetime.now(),
        'updated_at': datetime.datetime.now(),
    })
    return {"code": code}


@router.post("/xo/join", summary="Join a noughts and crosses game", tags=["noughts-and-crosses"])
def xo_join(response: Response, code: str, user=Depends(auth)):
    game_doc = db.collection('games').where('code', '==', code).get()
    if not game_doc:
        response.status_code = 404
        return {"error": "Game not found"}
    game = game_doc[0].to_dict()

    if game['status'] != 'waiting':
        response.status_code = 400
        return {"error": "Game is in progress"}
    elif user['id'] in game['players']:
        response.status_code = 400
        return {"error": "You are already in this game"}
    else:
        game['players'].append(user['id'])
        game['status'] = 'playing'
        game['updated_at'] = datetime.datetime.now()
        db.collection('games').document(game['id']).set(game)
        return {"success": True}


@router.get("/xo/status", summary="Get the status of a noughts and crosses game", tags=["noughts-and-crosses"])
def xo_status(response: Response, code: str):
    game = get_game(code)
    if not game:
        response.status_code = 404
        return {"error": "Game not found"}

    board = game['board']
    game['board'] = [[board[i], board[i+1], board[i+2]] for i in range(0, len(board), 3)]

    game.pop('id')
    game.pop('created_at')
    game.pop('updated_at')
    game.pop('type')
    game.pop('status')
    if not game['winner']:
        game.pop('winner')
    return game


@router.post("/xo/move", summary="Make a move in a noughts and crosses game", tags=["noughts-and-crosses"])
def xo_move(response: Response, code: str, position: int, user=Depends(auth)):
    game = get_game(code)
    user_id = user['id']
    user_turn = game['turn'] % 2
    if not game:
        response.status_code = 404
        return {"error": "Game not found"}
    elif game['status'] != 'playing':
        response.status_code = 400
        return {"error": "Game is not in progress"}
    elif user_id not in game['players']:
        response.status_code = 400
        return {"error": "You are not in this game"}
    elif game['players'][user_turn] == user_id:
        response.status_code = 400
        return {"error": "It's not your turn"}
    elif position not in range(1, 10):
        response.status_code = 400
        return {"error": "Position must be between 1 and 9"}
    elif game['board'][position - 1] != '-':
        response.status_code = 400
        return {"error": "Position is already taken"}
    else:
        board = game['board']
        board[position - 1] = 'O' if user_turn == 0 else 'X'
        winner = check_winner(board)
        if winner:
            if winner == 'X':
                game['winner'] = game['players'][0]
            elif winner == 'O':
                game['winner'] = game['players'][1]
            game['status'] = 'finished'
        game['board'] = board
        game['turn'] += 1
        game['turn_count'] += 1
        game['updated_at'] = datetime.datetime.now()
        db.collection('games').document(game['id']).set(game)
        return {"success": True}


def get_game(code: str):
    game_doc = db.collection('games').where('code', '==', code).get()
    if game_doc:
        return game_doc[0].to_dict()
    else:
        return None


def check_winner(board):
    if board[0] == board[1] == board[2] and board[0] != '-':
        return board[0]
    elif board[3] == board[4] == board[5] and board[3] != '-':
        return board[3]
    elif board[6] == board[7] == board[8] and board[6] != '-':
        return board[6]
    elif board[0] == board[3] == board[6] and board[0] != '-':
        return board[0]
    elif board[1] == board[4] == board[7] and board[1] != '-':
        return board[1]
    elif board[2] == board[5] == board[8] and board[2] != '-':
        return board[2]
    elif board[0] == board[4] == board[8] and board[0] != '-':
        return board[0]
    elif board[2] == board[4] == board[6] and board[2] != '-':
        return board[2]
    else:
        return None