from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select,func
from sqlalchemy.exc import IntegrityError
from models.cricketplayer_model import CricketPlayer
from schemas.cricketplayer_schema import CricketPlayerCreate,CricketPlayerUpdate
from config.logger import logger


# 1. Register a new cricket player. 
def create_player(db:Session,data):
    player=CricketPlayer(**data.model_dump())
    db.add(player)
    try:
        db.commit()
        db.refresh(player)
        logger.info(f"Player with Id {player.player_id} created successfully")
        return player
    
    except IntegrityError:
        db.rollback()
        logger.warning("Duplicate Player Id")
        raise HTTPException(status_code=409,detail="Player already exists")
    
    except Exception:
        db.rollback()
        logger.exception("Unexpected error occured while creating player")
        raise HTTPException(status_code=500,detail="Internal Server Error")


# 2. List all players with pagination. 
def get_all_players(db:Session,skip:int,limit:int):
    try:
        query=select(CricketPlayer).offset(skip).limit(limit)
        players=db.scalars(query).all() 
        logger.info(f"Successfully retrieved {len(players)} players")
        return players
    
    except Exception:
        logger.exception("Unexpected error occured while fetching players")
        raise HTTPException(status_code=500,detail="Internal Server Error")


# 3. Find a player by player ID. 
def get_player_by_id(db:Session,player_id:int):
     player=db.get(CricketPlayer,player_id)
     if player is None:
         logger.warning(f"No player with id {player_id} found")
         raise HTTPException(status_code=404,detail="Player Not Found")
     
     logger.info(f"Player with id {player_id} retrieved successfully")
     return player


# 4. Update player match statistics. 
def update_player_match_statistics(db:Session,player_id:int,data):
    player=get_player_by_id(db,player_id)
    for key,value in data.model_dump().items():
        setattr(player,key,value)
    try:
        db.commit()
        db.refresh(player)
        logger.info(f"Player with Id {player_id} updated successfully")
        return player
    except IntegrityError:
        db.rollback()
        logger.warning(f"Database constraint violation while updating player {player_id}")
        raise

    except Exception:
        db.rollback()
        logger.exception(f"Unexpected error while updating player {player_id}")
        raise HTTPException(status_code=500,detail="Internal Server Error")


# 5. Delete a player. 
def delete_player(db:Session,player_id:int):
    player=get_player_by_id(db,player_id)
    try:
        db.delete(player)
        db.commit()
        logger.info(f"Player with id {player_id} deleted successfully")
        return True
    
    except Exception:
        db.rollback()
        logger.exception(f"Unexpected error while deleting player with Id {player_id}")
        raise HTTPException(status_code=500,detail="Internal Server Error")


# 6. Filter players by team. 
def get_players_by_team(db:Session,team_name:str):

    query=select(CricketPlayer).where(CricketPlayer.team_name==team_name)
    players=db.scalars(query).all()

    if not players:
        logger.warning(f"No players found in team {team_name}")
        raise HTTPException(status_code=404,detail="No players found in this team")
    
    logger.info(f"Retrieved {len(players)} players from the team {team_name}")
    return players 

# 7. List all-rounders with at least 10 wickets. 
def get_all_rounders_with_wickets(db:Session):
    try:
        query=select(CricketPlayer).where(CricketPlayer.role=="All-Rounder", CricketPlayer.wickets_taken>=10)
        players=db.scalars(query).all()

        if not players:
           logger.warning("No all-rounders with at least 10 wickets found")
           raise HTTPException(status_code=404,detail="All-rounders with at least 10 wickets not found")
        logger.info(f"Retrieved {len(players)} all-rounders with at least 10 wickets")
        return players
    
    except HTTPException:
        raise

    except Exception:
        logger.exception("Unexpected error while fetching all-rounders")
        raise HTTPException(status_code=500,detail="Internal Server Error")

# 8. Return the top five run scorers.
def get_top_five_run_scorers(db:Session):
    try:
        query=select(CricketPlayer).order_by(CricketPlayer.total_runs.desc()).limit(5)
        top_five_scorers=db.scalars(query).all()
        logger.info("Successfully retrieved top five run scorers")
        return top_five_scorers
    except Exception:
        logger.exception("Unexpected error while fetching top five run scorers")
        raise HTTPException(status_code=500,detail="Internal Server Error")

# 9. Calculate batting strike rate as runs divided by balls faced multiplied by 100. 
def calculate_strike_rate(db:Session,player_id:int):

    player=get_player_by_id(db,player_id)

    try:
        if player.balls_faced==0:
            strike_rate=0
        else:
            strike_rate=(player.total_runs/player.balls_faced)*100
        logger.info(f"Strike rate calculated successfully for player {player_id}")
        return{
                  "player_id":player.player_id,
                  "player_name":player.player_name,
                  "strike_rate":round(strike_rate,2)
            }
            
    except Exception:
        logger.exception(f"Unexpected error while calculating strike rate for player {player_id}")
        raise HTTPException(status_code=500,detail="Internal Server Error")


# 10. Calculate total runs and wickets for each team. 
def get_team_runs_and_wickets(db:Session):

    try:
        query=select(CricketPlayer.team_name,func.sum(CricketPlayer.total_runs).label("total_runs"),
              func.sum(CricketPlayer.wickets_taken).label("total_wickets")).group_by(CricketPlayer.team_name)

        stats=db.execute(query).all()
        result=[]
        for team,runs,wickets in stats:
            result.append({
                "team_name":team,
                "total_runs":runs,
                "total_wickets":wickets
            })
        logger.info(f"Successfully retrieved runs and wickets statistics for {len(result)} teams")
        return result
    except Exception:
        logger.exception("Unexpected error while calculating team runs and wickets")
        raise HTTPException(status_code=500,detail="Internal Server Error")




             
    
          

    





    

