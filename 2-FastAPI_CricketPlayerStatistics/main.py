#imports
from fastapi import FastAPI
from config.database import Base,engine,SessionLocal
from services import cricketplayer_service as service
from schemas.cricketplayer_schema import CricketPlayerCreate,CricketPlayerUpdate,CricketPlayerResponse


app=FastAPI(title="Cricket Player Statistics API ")

Base.metadata.create_all(bind=engine)


@app.post("/createPlayers",response_model=CricketPlayerResponse,status_code=201)
def create_player(player:CricketPlayerCreate):
    db=SessionLocal()
    try:
        return service.create_player(db,player)
    finally:
        db.close()


@app.get("/getAllPlayers",response_model=list[CricketPlayerResponse])
def get_all_players(skip:int=0,limit:int=10):
    db=SessionLocal()
    try:
        return service.get_all_players(db,skip,limit)
    finally:
        db.close()


@app.get("/getPlayerById/{player_id}",response_model=CricketPlayerResponse)
def get_player_by_id(player_id:int):
    db=SessionLocal()
    try:
        return service.get_player_by_id(db,player_id)
    finally:
        db.close()


@app.put("/updateMatchStatistics/{player_id}",response_model=CricketPlayerResponse)
def update_player_match_statistics(player_id:int,player:CricketPlayerUpdate):
    db=SessionLocal()
    try:
        return service.update_player_match_statistics(db,player_id,player)
    finally:
        db.close()


@app.delete("/deletePlayer/{player_id}")
def delete_player(player_id:int):
    db=SessionLocal()
    try:
        return service.delete_player(db,player_id)
    finally:
        db.close()


@app.get("/getPlayersByTeam/{team_name}",response_model=list[CricketPlayerResponse])
def get_players_by_team(team_name:str):
    db=SessionLocal()
    try:
        return service.get_players_by_team(db,team_name)
    finally:
        db.close()


@app.get("/getAllRoundersWithWickets",response_model=list[CricketPlayerResponse])
def get_all_rounders_with_wickets():
    db=SessionLocal()
    try:
        return service.get_all_rounders_with_wickets(db)
    finally:
        db.close()


@app.get("/getTopFiveRunScorers",response_model=list[CricketPlayerResponse])
def get_top_five_run_scorers():
    db=SessionLocal()
    try:
        return service.get_top_five_run_scorers(db)
    finally:
        db.close()


@app.get("/strikeRate/{player_id}")
def calculate_strike_rate(player_id:int):
    db=SessionLocal()
    try:
        return service.calculate_strike_rate(db,player_id)
    finally:
        db.close()


@app.get("/teamRunsAndWickets")
def get_team_runs_and_wickets():
    db=SessionLocal()
    try:
        return service.get_team_runs_and_wickets(db)
    finally:
        db.close()
        