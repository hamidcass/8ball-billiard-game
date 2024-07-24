import phylib;
import os;
import sqlite3;
import math;

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH
SIM_RATE = phylib.PHYLIB_SIM_RATE
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON
DRAG = phylib.PHYLIB_DRAG
MAX_TIME = phylib.PHYLIB_MAX_TIME
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS

HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />"""

FOOTER = """</svg>\n"""

FRAME_INTERVAL = 0.01

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;


    # add an svg method here
    def svg(self):
        pos = self.obj.still_ball.pos
        number = self.obj.still_ball.number
        return """ <circle cx="{}" cy="{}" r="{}" fill="{}" />\n""".format(pos.x,pos.y, BALL_RADIUS, BALL_COLOURS[number])

class RollingBall( phylib.phylib_object ):
    """
    Python RollingBall class.
    """

    def __init__( self, number, pos, vel, acc ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel, acc, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = RollingBall;

    def svg(self):
        pos = self.obj.rolling_ball.pos
        vel = self.obj.rolling_ball.vel
        acc = self.obj.rolling_ball.acc
        number = self.obj.rolling_ball.number
        return """ <circle cx="{}" cy="{}" r="{}" fill="{}" />\n""".format(pos.x,pos.y, BALL_RADIUS, BALL_COLOURS[number])

class Hole( phylib.phylib_object ):
    """
    Python Hole class.
    """

    def __init__( self, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HOLE, 
                                       0, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = Hole;

    def svg(self):
        pos = self.obj.hole.pos
        return """ <circle cx="{}" cy="{}" r="{}" fill="black" />\n""".format(pos.x,pos.y, HOLE_RADIUS, BALL_COLOURS[1])

class HCushion( phylib.phylib_object ):
    """
    Python HCushion class.
    """

    def __init__( self, y ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HCUSHION, 
                                       0, 
                                       None, None, None, 
                                       0.0, y );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = HCushion;

        

       

    def svg(self):
        if self.obj.hcushion.y == 0:
            return """ <rect width="1400" height="25" x="-25" y="-25" fill="darkgreen" />\n"""
        else:
            return """ <rect width="1400" height="25" x="-25" y="2700" fill="darkgreen" />\n"""

class VCushion( phylib.phylib_object ):
    """
    Python HCushion class.
    """

    def __init__( self, x ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_VCUSHION, 
                                       0, 
                                       None, None, None, 
                                       x, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = VCushion;

    def svg(self):
        if self.obj.vcushion.x == 0:
            return """ <rect width="25" height="2750" x="-25" y="-25" fill="darkgreen" />\n"""
        else:
            return """ <rect width="25" height="2750" x="1350" y="-25" fill="darkgreen" />\n"""


################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;

            #print(result)

        return result;

    # add svg method here
    def svg(self):

        #if self != None:
            string = ""
            string += HEADER

            for obj in self:
                if obj != None:
                    
                    string += obj.svg()
                  

            string+=FOOTER

            return string

    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                        Coordinate(0,0),
                                        Coordinate(0,0),
                                        Coordinate(0,0) );

             
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );
            

                # add ball to table
                new += new_ball;

            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                            Coordinate( ball.obj.still_ball.pos.x,
                            ball.obj.still_ball.pos.y ) );

                # add ball to table
                new += new_ball;
        # return table
        return new;

    def cueBall( self ):
        for item in self:
            if isinstance( item, StillBall ):
                if item.obj.still_ball.number == 0:
                    return item
            elif isinstance( item, RollingBall ):
                
                if item.obj.rolling_ball.number == 0:
                    return item
                
        
################################################################################

class Database():
    """
    Database class.
    """

    conn: sqlite3.Connection

    def __init__( self, reset=False ):

        if reset == True:
            if os.path.exists( 'phylib.db' ):
                os.remove( 'phylib.db' )

        #open database connection to 
        self.conn = sqlite3.connect( 'phylib.db' )
        

    def createDB( self ):


        #print("Establishing cursor...")
        cur = self.conn.cursor()

        #create tables

        #------------BALL-------------:



        #print("Creating Ball table...")
        #create table
        cur.execute( """

        CREATE TABLE IF NOT EXISTS Ball (
            BALLID      INTEGER    NOT NULL,
            BALLNO      INTEGER    NOT NULL,
            XPOS        FLOAT      NOT NULL,                              
            YPOS        FLOAT      NOT NULL,
            XVEL        FLOAT,
            YVEL        FLOAT,
            PRIMARY KEY (BALLID AUTOINCREMENT)  );
        
        """ )
            

        
        #------------TTABLE-------------:

        #print("Creating TTable table...")

        #create table
        cur.execute( """

        CREATE TABLE IF NOT EXISTS TTable (
            TABLEID     INTEGER     NOT NULL,
            TIME        FLOAT       NOT NULL,
            PRIMARY KEY (TABLEID AUTOINCREMENT));
        
        """ )        

        #------------BALLTABLE-------------:

        #print("Creating BallTable table...")

        #create table
        cur.execute( """

        CREATE TABLE IF NOT EXISTS BallTable (
            BALLID      INTEGER     NOT NULL,
            TABLEID     INTEGER     NOT NULL,
            FOREIGN KEY (BALLID) REFERENCES Ball (BALLID),
            FOREIGN KEY (TABLEID) REFERENCES TTable (TABLEID)  );
        
        """ )
            
        #------------SHOT-------------:

        #print("Creating Shot table...")

        cur.execute( """

        CREATE TABLE IF NOT EXISTS Shot (
            SHOTID      INTEGER     NOT NULL,
            PLAYERID    INTEGER     NOT NULL,
            GAMEID      INTEGER     NOT NULL,
            PRIMARY KEY (SHOTID AUTOINCREMENT),
            FOREIGN KEY (PLAYERID) REFERENCES Player (PLAYERID),
            FOREIGN KEY (GAMEID)   REFERENCES Game (GAMEID)  );
        
        """ )
            

      




        #------------TABLESHOT-------------:

        #print("Creating TableShot table...")

        cur.execute( """

        CREATE TABLE IF NOT EXISTS TableShot (
            TABLEID      INTEGER     NOT NULL,
            SHOTID       INTEGER     NOT NULL,
            FOREIGN KEY (TABLEID) REFERENCES TTable (TABLEID),
            FOREIGN KEY (SHOTID) REFERENCES Shot (SHOTID));
        
        """ )        

        
        #------------GAME-------------:

        #print("Creating Game table...")

        cur.execute( """

        CREATE TABLE IF NOT EXISTS Game (
            GAMEID      INTEGER         NOT NULL,
            GAMENAME    VARCHAR(64)     NOT NULL,
            PRIMARY KEY (GAMEID AUTOINCREMENT));
        
        """ )


        #------------PLAYER-------------:

        #print("Creating Player table...")

        cur.execute( """

        CREATE TABLE IF NOT EXISTS Player (
            PLAYERID      INTEGER     NOT NULL,
            GAMEID        INTEGER     NOT NULL,
            PLAYERNAME    VARCHAR(64) NOT NULL,
            PRIMARY KEY (PLAYERID AUTOINCREMENT)
            FOREIGN KEY (GAMEID) REFERENCES Game (GAMEID) );
        
        """ )

        #print("All tables made...")

        
        cur.close()
        self.conn.commit()

        #print("Committed...")
        #self.conn.close()

    def readTable( self, tableID ):

        #print("Establishing cursor...")
        cur = self.conn.cursor()

        #create the table (no balls)
        table = Table()

        #get balls in db

        cur.execute( """
        SELECT Ball.*
        FROM   Ball
        JOIN BallTable ON Ball.BALLID = BallTable.BALLID
        WHERE BallTable.TABLEID = ?;     
        """,(tableID + 1,))




        rows = cur.fetchall()

        #print("Rows", rows)

        if not rows:
            
            return None

        # Print the fetched rows
        ##print("All balls on table:")

        for ball in rows:

            ###print(ball, "[4]: ", ball[4])
            
            #still ball
            if (ball[4] is None and ball[5] is None) or (ball[4] == 0 and ball[5] == 0):
                #print("Ball is not moving!")

                ballNum = ball[1]
                ballPos = Coordinate(ball[2], ball[3])
                newBall = StillBall(ballNum, ballPos)
                table += newBall

                #print("Still ball added to table")

            #rolling ball
            else:
             
                ballNum = ball[1]
                ballPos = Coordinate(ball[2], ball[3])
                ballVel = Coordinate(ball[4], ball[5])

                #get acc

                speed = phylib.phylib_length(ballVel)

                acc_x = 0
                acc_y = 0


                if speed > phylib.PHYLIB_VEL_EPSILON:
           
                    acc_x = -(ball[4]) / speed * phylib.PHYLIB_DRAG
                    acc_y = -(ball[5]) / speed * phylib.PHYLIB_DRAG

                ballAcc = Coordinate(acc_x,acc_y)

                newBall = RollingBall(ballNum, ballPos, ballVel, ballAcc)
                table += newBall

                #print("Rolling ball added to table")

        cur.execute( """
        SELECT TTable.TIME
        FROM   TTable
        WHERE TTable.TABLEID = ?;     
        """,(tableID + 1,))

        time = cur.fetchall()[0][0]
        table.time = time
        
            

        cur.close()
        self.conn.commit()

        #return table object
        return table

    def writeTable( self, table):

        

        #print("Establishing cursor...")
        cur = self.conn.cursor()

        tableTime = table.time

        #print("Table time: ",tableTime)
      

        #store the table (time)

        cur.execute( """
        INSERT
        INTO TTable (TIME)
        VALUES    (?);       

        """,(tableTime,))

        #save table id
        cur.execute("""
        SELECT last_insert_rowid() 
        AS TABLEID;
        """)

        tableId = cur.fetchone()[0]



        #store balls

        

        
        for i in table:
           
            if isinstance( i, StillBall ):
                ##print("Still ball found.")

                #Ball

                cur.execute( """
                INSERT
                INTO Ball (BALLNO, XPOS, YPOS)
                VALUES    (?,      ?,    ?);       

                """,(i.obj.still_ball.number, i.obj.still_ball.pos.x, i.obj.still_ball.pos.y))

                #save ball id
                cur.execute("""
                SELECT last_insert_rowid() 
                AS BALLID;
                """)
                ballId = cur.fetchone()[0]

                #BallTable
                cur.execute( """
                INSERT
                INTO BallTable (BALLID, TABLEID)
                VALUES    (     ?,      ?);       

                """,(ballId, tableId))           

            elif isinstance( i, RollingBall ):
                ##print("Rolling ball found.")

                cur.execute( """
                INSERT
                INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL)
                VALUES    (?,      ?,    ?,    ?,    ?);       

                """,(i.obj.rolling_ball.number, i.obj.rolling_ball.pos.x, i.obj.rolling_ball.pos.y, i.obj.rolling_ball.vel.x, i.obj.rolling_ball.vel.y))
                
                #save ball id
                cur.execute("""
                SELECT last_insert_rowid() 
                AS BALLID;
                """)
                ballId = cur.fetchone()[0]
                ##print("TableID: ",tableId)

                #BallTable
                cur.execute( """
                INSERT
                INTO BallTable (BALLID, TABLEID)
                VALUES    (     ?,      ?);       

                """,(ballId, tableId))

        cur.close()
        #self.conn.commit()
        return tableId - 1

    def close( self ):
        self.conn.commit()
        self.conn.close()

    def getConn( self ):
        return self.conn

    def checkTableTime(self, time):
        #print("Establishing cursor...")
        cur = self.conn.cursor()
        
        #get balls in db
     
        #round the time to 2 decimal places, TODO: change to three decimal places?
        newTime = round(float(time),2)
        #print("Requested time: ", newTime)
        #nrange = 0.01
        #print(newTime)

        #print("In func: time is ", time, round(time,2))

        cur.execute( """
        SELECT TTable.TABLEID
        FROM   TTable
        WHERE ROUND(TTable.TIME, 2) = ?;     
        """,(newTime, ))

        
        rows = cur.fetchall()
        #print(rows)

      
        if rows:

            table_ID = rows[0][0]
        

        #print(table_ID)

        if not rows:
            print("No table exists, returning None")
            cur.close()
            self.conn.commit()

            return None

        return table_ID

        

        cur.close()
        self.conn.commit()
        return table

    def getLastTable(self):

        cur = self.conn.cursor()
        cur.execute( """
        SELECT TTable.TABLEID
        FROM   TTable;     
        """)

        last_id = cur.fetchall()[-1][0]
        cur.close()
        self.conn.commit()
        
        return last_id
    def getLastTime(self):

        cur = self.conn.cursor()

        cur.execute( """
        SELECT TTable.TIME
        FROM   TTable;     
        """)

        last_time = cur.fetchall()[-1][0]

        cur.close()
        self.conn.commit()

        return last_time




class Game():
    def __init__( self, gameID=None, gameName=None, player1Name=None, player2Name=None ):

        #open database connection
        #self.conn = sqlite3.connect( 'phylib.db' )
        #TODO: change to false
        self.db = Database()
        self.db.createDB()
        self.conn = self.db.getConn()

        #print("Database connected")
        #print(gameName, player1Name, player2Name)

        version = 0

    
        if isinstance(gameID, int) and gameName is None and player1Name is None and player2Name is None:
            version = 1
        elif gameID is None and isinstance(gameName, str) and isinstance(player1Name, str) and isinstance(player2Name, str):
            version = 2
        else:
            version = 0

        if version == 0:
            raise TypeError("Invalid Arguments")

       
        cur = self.conn.cursor()
        #print("CONNECTION")

        #Loading a game
        if version == 1:
            print("loading saved game")

            gameID += 1

            cur.execute("""
            SELECT Game.GAMENAME, Player.PLAYERNAME
            FROM GAME
            JOIN Player ON Game.GAMEID = Player.GAMEID
            WHERE Game.GAMEID = ?;            
            """,(gameID,))

            #print("Rows:")
            rows = cur.fetchall()
            #print(rows)
            if not rows:
                self.gameID = gameID
                self.gameName = gameName
                self.player1Name = player1Name
                self.player2Name = player2Name

        if version == 2:
            print("Starting a new game")

            self.gameName = gameName
            self.player1Name = player1Name
            self.player2Name = player2Name

            #add game and players to Game and Player tables

            cur.execute("""
            INSERT
            INTO Game (GAMENAME)
            VALUES    (?);        
            """,(self.gameName,))

            print("inserted into game table")

            #TEST RETRIVE GAME ID
            cur.execute("""
            SELECT Game.GAMEID
            FROM Game
            WHERE Game.GAMENAME = ?;
            """,(self.gameName,))

            gameId = cur.fetchall()[0][0]
            print("Game ID: ", gameId)

            cur.execute("""
            INSERT
            INTO Player (PLAYERNAME, GAMEID)
            VALUES       (?, ?)
            """,(self.player1Name,gameId))

            cur.execute("""
            INSERT
            INTO Player (PLAYERNAME, GAMEID)
            VALUES       (?,?)
            """,(self.player2Name,gameId))



            #----TEST------
            cur.execute("""
            SELECT *
            FROM Player
            """)

            players = cur.fetchall()

            #print(players)

                #CLOSE CURSOR------------------
                #cur.close()
            self.conn.commit()
       


    def shoot( self, gameName, playerName, table, xvel, yvel ):

        

        #print("Establishing cursor...")
        cur = self.conn.cursor()

        #look up playerName in Player table
        cur.execute("""
        SELECT Player.PLAYERID
        FROM Player
        WHERE Player.PLAYERNAME = ?;
        """,(playerName,))

        fetchedPlayerID = cur.fetchall()[0][0]

        print("1")

        #print("Player ID retrieved: ", fetchedPlayerID)

        #get gameID
        cur.execute("""
        SELECT Player.GAMEID
        FROM Player
        WHERE Player.PLAYERNAME = ?;
        """,(playerName,))

        fetchedGameID = cur.fetchall()[0][0]

        print("2")

        #print("Fetched game id: ", fetchedGameID)

        #add entry to Shot table
        cur.execute("""
            INSERT
            INTO Shot (PLAYERID, GAMEID)
            VALUES    (?,        ?);
            """,(fetchedPlayerID, fetchedGameID))

        print("3")

        #get shotID
        cur.execute("""
            SELECT Shot.SHOTID
            FROM Shot 
            WHERE PLAYERID = ? AND GAMEID = ?;
            """,(fetchedPlayerID, fetchedGameID))



        fetchedShotID = cur.fetchall()[0][0]

        print("4")

        #print("Fetched shot id: ", fetchedShotID)

        
        

        #find the cue ball
        #cueBall = table.cueBall()
        
        for item in table:
            if isinstance( item, StillBall ):
                if item.obj.still_ball.number == 0:
                    cueBall = item
                    #print("Found cue ball!")
            elif isinstance( item, RollingBall ):
                if item.obj.rolling_ball.number == 0:
                    #print("Found cue ball")
                    cueBall = item

        print("5")


        #store pos
        if isinstance( cueBall, StillBall ):
            cuePosX = cueBall.obj.still_ball.pos.x
            cuePosY = cueBall.obj.still_ball.pos.y
         

        elif isinstance( cueBall, RollingBall ):
           
            cuePosX = cueBall.obj.rolling_ball.pos.x
            cuePosY = cueBall.obj.rolling_ball.pos.y         
        
        cueBall.type = phylib.PHYLIB_ROLLING_BALL
        cueBall.obj.rolling_ball.number = 0
        cueBall.obj.rolling_ball.pos.x = cuePosX
        cueBall.obj.rolling_ball.pos.y = cuePosY

        cueBall.obj.rolling_ball.vel.x = xvel
        cueBall.obj.rolling_ball.vel.y = yvel

        #get acc
        ballVel = Coordinate(xvel,yvel)
        speed = phylib.phylib_length(ballVel)


        acc_x = 0
        acc_y = 0


        if speed > phylib.PHYLIB_VEL_EPSILON:
           
            acc_x = -(xvel) / speed * phylib.PHYLIB_DRAG
            acc_y = -(yvel) / speed * phylib.PHYLIB_DRAG

        cueBall.obj.rolling_ball.acc.x = acc_x
        cueBall.obj.rolling_ball.acc.y = acc_y

       
       # db = Database()
       # db.createDB()

        #print("Pos: ", cuePosX, ", ", cuePosY )
        #print("Vel: ", xvel, ", ", yvel )
        #print("Acc: ", acc_x, ", ", acc_y )

        #print("Cue ball:")
        #print(cueBall)

        #print("Starting segment")
        #print(table)
       
       
        #call segment
        newTable = table

        counter = 0

        while(table): 

            startTime = table.time         
            table = table.segment()
           
            if table is not None:
                endTime = table.time   
                i = math.floor((endTime - startTime)/FRAME_INTERVAL)

                for frame in range(i):

                    counter+=1
             
                    table3 = newTable.roll(frame*FRAME_INTERVAL)
                    table3.time = startTime + frame*FRAME_INTERVAL
                    #save to sql tables
                    tableId = self.db.writeTable(table3)

                    cur.execute("""
                    INSERT 
                    INTO TableShot (TABLEID, SHOTID)
                    VALUES         (?,?)
                    """,(tableId,fetchedShotID))
                    #print("Shot!")

                newTable = table
           

        
                    

                

                

        #print(counter)

        cur.close()
        self.conn.commit()
        #self.conn.close()
        return fetchedShotID



   






            




        
        
                
                
                











