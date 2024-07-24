import sys; # used to get argv
import cgi;
import os;
import requests;
import random;
import urllib;
import math;
import json;

import Physics;
import phylib;
import sqlite3;

from http.server import HTTPServer,  BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qsl;

def nudge():
    return random.uniform( -1.5, 1.5 );

def write_svg( table_id, table ):
    #print("WRITING TO ", "table%02d.svg" % table_id )
    with open( "table%02d.svg" % table_id, "w" ) as fp:
        fp.write( table.svg() );

def delete_svg_files(folder_path):
    #print(folder_path)

    for file in os.listdir(folder_path):
        #print(file)
        if file.endswith(".svg"):
            file_path = os.path.join(folder_path, file)
            os.remove(file_path)




class MyHandler(BaseHTTPRequestHandler):

    table = None
    players = None
    p1 = None
    p2 = None
    active_player = None
    game = None
    shots_made = 0
    low = None
    high = None
    event_message = "Test"   #message sent to front end based on previous play

    table_id = 0
    start_time = 0

    def do_GET(self):
 
        if self.path == "/":
            #code
            html = open( '.'+"/index.html" );
            html_content = html.read();

            css = open('.' + "/style.css")
            css_content = css.read()

            all_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>8-Ball Pool Game</title>
                <style>
                    {css_content}
                </style>

            </head>
            <body>
                {html_content}                
            </body>
            </html>

            """


            self.send_response(200)
            self.send_header( "Content-type", "text/html" )
            self.send_header( "Content-length", len( all_content ) )
            self.end_headers()

            self.wfile.write( bytes( all_content, "utf-8" ) )
            html.close()
            css.close()
        
        elif self.path == "/shot.html":
            print("Shot page")
        

        
        elif self.path.startswith("/table-") and self.path.endswith(".svg"):

      

            if os.path.exists('.'+ self.path):
                fp = open( '.'+self.path );
                content = fp.read();

                # generate the headers
                self.send_response( 200 ); # OK
                self.send_header( "Content-type", "image/svg+xml" );
                self.send_header( "Content-length", len( content ) );
                self.end_headers();

                self.wfile.write( bytes( content, "utf-8" ) );
                fp.close();
            else:
                print("error")
                self.send_error( 404, "Invalid file name" ); #invalid svg name


    def do_POST(self):

   

        if self.path == "/game.html":
            
            #recive form data from shot.html

            form = cgi.FieldStorage( fp=self.rfile,
                                     headers=self.headers,
                                     environ = { 'REQUEST_METHOD': 'POST',
                                                 'CONTENT_TYPE': 
                                                   self.headers['Content-Type'],
                                               } 
                                    );

       

            p1_name = form.getvalue('p1_name')
            p2_name = form.getvalue('p2_name')

            MyHandler.p1 = p1_name
            MyHandler.p2 = p2_name

            #TODO: function: save to database


            #decide who goes first
            MyHandler.players = [p1_name, p2_name]
            MyHandler.active_player = random.choice(MyHandler.players)  #this is the player whos turn it is

         


  
            MyHandler.table = Physics.Table()


           

            pos = Physics.Coordinate( 
                Physics.TABLE_WIDTH / 2.0,
                Physics.TABLE_LENGTH / 4.0,
                );

            sb = Physics.StillBall( 15, pos );
            MyHandler.table += sb

            pos = Physics.Coordinate( 
                645,
                622
                );

            sb = Physics.StillBall( 10, pos );
            MyHandler.table += sb

            pos = Physics.Coordinate( 
                705,
                622 + nudge()
                );

            sb = Physics.StillBall( 2, pos );
            MyHandler.table += sb

            pos = Physics.Coordinate( 
                733,
                566 + nudge()
                );

            sb = Physics.StillBall( 9, pos );
            MyHandler.table += sb

            pos = Physics.Coordinate( 
                615,
                566 + nudge()
                );

            sb = Physics.StillBall( 1, pos );
            MyHandler.table += sb

            pos = Physics.Coordinate( 
                705,
                510 + nudge()
                );

            sb = Physics.StillBall( 7, pos );
            MyHandler.table += sb

            pos = Physics.Coordinate( 
                765,
                510 + nudge()
                );

            sb = Physics.StillBall( 13, pos );
            MyHandler.table += sb

            pos = Physics.Coordinate( 
                675,
                566 + nudge()
                );

            sb = Physics.StillBall( 8, pos );
            MyHandler.table += sb

            pos = Physics.Coordinate( 
                645,
                508 + nudge()
                );

            sb = Physics.StillBall( 6, pos );
            MyHandler.table += sb

            pos = Physics.Coordinate( 
                585,
                508 + nudge()
                );

            sb = Physics.StillBall( 11, pos );
            MyHandler.table += sb

            pos = Physics.Coordinate( 
                550,
                455 + nudge()
                );

            sb = Physics.StillBall( 5, pos );
            MyHandler.table += sb

            pos = Physics.Coordinate( 
                615,
                455 + nudge()
                );

            sb = Physics.StillBall( 12, pos );
            MyHandler.table += sb

            pos = Physics.Coordinate( 
                677,
                455 + nudge()
                );

            sb = Physics.StillBall( 14, pos );
            MyHandler.table += sb

            pos = Physics.Coordinate( 
                800,
                455 + nudge()
                );

            sb = Physics.StillBall( 3, pos );
            MyHandler.table += sb

            pos = Physics.Coordinate( 
                737,
                455 + nudge()
                );

            sb = Physics.StillBall( 4, pos );
            MyHandler.table += sb


            # cue ball also still
            pos = Physics.Coordinate( Physics.TABLE_WIDTH/2.0 + random.uniform( -3.0, 3.0 ),
                          Physics.TABLE_LENGTH - Physics.TABLE_WIDTH/2.0 );
            sb  = Physics.StillBall( 0, pos );

            MyHandler.table += sb

            #STARTING GAME
            #TODO: change game name 

            MyHandler.game = Physics.Game( gameName="Game 01", player1Name=p1_name, player2Name=p2_name );
            print("Game logged")
            

            with open( "table00.svg", "w" ) as fp:
                fp.write( MyHandler.table.svg() );
        


            #Return new webpage to server

            #code
            html = open( '.'+"/game.html" );
            html_content = html.read();

            css = open('.' + "/style.css")
            css_content = css.read()

            start_table = open('.' + "/table00.svg")
            #tableSvg = start_table.read()
            tableSvg = start_table.read()

            jquery = open("." + "/script.js")
            jquery_content = jquery.read()

            all_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>8-Ball Pool Game</title>
                <style>
                    {css_content}
                </style>
                <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js">
                </script>
            </head>
            <body>
            <canvas id="canvas"></canvas>
                <div id='title_container'>
                    <h1 id='p1'>8-ball Pool Game</h1>
                </div>
                <div id='curr_div'>
                    <h1 id='curr'>Current turn: {MyHandler.active_player}</h1>
                </div>
                <div id='message_div'>
                    <h1 id='message'> </h1>
                </div>
                <div class="game">
                
                    <div class="svg_container">                     
                        
                        {tableSvg}
                    </div>
                </div>
              
                <script>
                    {jquery_content}
                </script>
            </body>
            </html>

            """

            self.send_response(200)
            self.send_header( "Content-type", "text/html" )
            self.send_header( "Content-length", len( all_content ) )
            self.end_headers()

            self.wfile.write( bytes( all_content, "utf-8" ) )
            html.close()
            css.close()

        elif self.path == "/shot.html":
            form = cgi.FieldStorage( fp=self.rfile,
                                     headers=self.headers,
                                     environ = { 'REQUEST_METHOD': 'POST',
                                                 'CONTENT_TYPE': 
                                                   self.headers['Content-Type'],
                                               } 
                                    );
            
            MyHandler.shots_made += 1

            x_vel = form.getvalue('x_vel')
            y_vel = form.getvalue('y_vel')
            current_player = form.getvalue('current_player')

            print("XVEL: ", x_vel)
            print("YVEL: ", y_vel)
           
            #print("BEFORE THE SHOT:")

            #print(MyHandler.table)
            print(MyHandler.active_player)
            print("Shooting:")

            #keep track of current balls on table
            cue_x = 0
            cue_y = 0

            curr_balls = []
            for obj in MyHandler.table:
                if obj:
                    #get white ball coord
                    if obj.obj.still_ball.number == 1:
                        cue_x = obj.obj.still_ball.pos.x
                        cue_y = obj.obj.still_ball.pos.y

                    if obj.type == 0: #if object on table is ball
                        curr_balls.append(obj.obj.still_ball.number)    
                        
                    elif obj.type == 1: 
                        curr_balls.append(obj.obj.rolling_ball.number)

            print("Current balls on table: ", curr_balls)

            #TODO: change to acutal game name
            shot_id = MyHandler.game.shoot( "Game 01", MyHandler.active_player, MyHandler.table, float(x_vel), float(y_vel) )

            #print("AFTER THE SHOT:")

            print(MyHandler.table)

            #fetch last table id
            #turn into table

            db = Physics.Database()
            conn = sqlite3.connect( 'phylib.db' )
            cur = conn.cursor()


            final_time = db.getLastTime()
            print("Final time: ", final_time)

            cur.execute("""
                SELECT TableShot.TABLEID
                FROM TableShot
                WHERE TableShot.SHOTID = ?;
            """,(shot_id,))

            table_ids = cur.fetchall()
            last_table_id = table_ids[-1][0]
            #print(last_table_id)

            #update existing table
            MyHandler.table = db.readTable(last_table_id)

            #figure out which balls dropped
            new_balls = []
            sunk_balls = []
            for obj in MyHandler.table:
                if obj:
                    if obj.type == 0: #if object on table is ball
                        new_balls.append(obj.obj.still_ball.number)    
                    
                    elif obj.type == 1: 
                        new_balls.append(obj.obj.rolling_ball.number)

            #sunk balls = curr_balls - new_balls
            sunk_balls = curr_balls
            for num in new_balls:
                sunk_balls.remove(num)

            print("Balls on table now: ", new_balls)
            print("Sunken Balls: ", sunk_balls)

            def changeTurn():
                print("Changing turn...")
                if MyHandler.active_player == MyHandler.p1:
                    MyHandler.active_player = MyHandler.p2
                else:
                    MyHandler.active_player = MyHandler.p1

            #apply rules

            game_over = 0
            winner = None
            game_lost = 0
            game_won = 0
            go_again = 0
            

            #on break:
            if MyHandler.shots_made == 1:

                print("It's the first shot")

                if not sunk_balls: 
                    print("No balls were sunk on break.")
                    changeTurn()
                else:
                    if 8 in sunk_balls:
                        print(MyHandler.active_player, " sunk the 8-ball and lost. Game over!")
                        game_lost = 1
                        #TODO: set winner

                    if 0 in sunk_balls:
                        #re add white to table
                        pos = Physics.Coordinate( 
                            cue_x,
                            cue_y
                        );

                        sb = Physics.StillBall( 0, pos );
                        MyHandler.table += sb

                        #remove from sunk balls
                        sunk_balls.remove(0)

                        if sunk_balls:  #if still more balls sunk
                            #check what type
                            if sunk_balls[0] < 8:
                                MyHandler.low = MyHandler.active_player
                                #set high
                                if MyHandler.low == MyHandler.p1:
                                    MyHandler.high = MyHandler.p2
                                else:
                                    MyHandler.high = MyHandler.p1
                            else:
                                MyHandler.high = MyHandler.active_player
                                #set low
                                if MyHandler.high == MyHandler.p1:
                                    MyHandler.low = MyHandler.p2
                                else:
                                    MyHandler.low = MyHandler.p1
                               


                        else: #only sunk white ball
                            changeTurn()

                    #white ball and black were NOT sunk
                    else: 
                        #only coloured balls sunk
                        if sunk_balls:  #if still more balls sunk
                            #check what type
                            if sunk_balls[0] < 8:
                                MyHandler.low = MyHandler.active_player
                                #set high
                                if MyHandler.low == MyHandler.p1:
                                    MyHandler.high = MyHandler.p2
                                else:
                                    MyHandler.high = MyHandler.p1


                            else:
                                MyHandler.high = MyHandler.active_player

                                #set high
                                if MyHandler.high == MyHandler.p1:
                                    MyHandler.low = MyHandler.p2
                                else:
                                    MyHandler.low = MyHandler.p1
                               


                         #no balls sunk
                        else:
                            print("No balls sunk on break")
                            changeTurn()

            #every turn thats not break
            else:
                #black ball sunk
                if 8 in sunk_balls:   #check this later
                    #check if it was the last ball or not
                    if MyHandler.low == MyHandler.active_player:
                        for i in sunk_balls:
                            if i < 8 and i != 0:
                                #game over current player lost
                                game_lost = 1
                                break
                        if game_lost == 0:
                            print(f"{active_player} wins!")
                            
                        else:
                            print(f"{active_player} loses (sunk 8 ball with other balls remaining!")
                            

                    elif MyHandler.high == MyHandler.active_player:
                        for i in sunk_balls:
                            if i > 8 and i != 0:
                                #game over current player lost
                                game_lost = 1

                        #game over current player wins 
                        if game_lost == 0:
                            print(f"{active_player} wins!")
                            
                        else:
                            print(f"{active_player} loses (sunk 8 ball with other balls remaining!")
                            

                if 0 in sunk_balls: 
                        print("Cue ball was sunk!")
                    #re add white to table
                        pos = Physics.Coordinate( 
                            cue_x,
                            cue_y
                        );

                        sb = Physics.StillBall( 0, pos );
                        MyHandler.table += sb

                        #remove from sunk balls
                        sunk_balls.remove(0)

                        if sunk_balls:  #if still more balls sunk
                            print("Coloured ball was sunk!")

                            #if no sides were selected (first ball sunk)
                            if not MyHandler.low:
                                #check what type
                                if sunk_balls[0] < 8:
                                    MyHandler.low = MyHandler.active_player

                                    #set high
                                    if MyHandler.low == MyHandler.p1:
                                        MyHandler.high = MyHandler.p2
                                    else:
                                        MyHandler.high = MyHandler.p1
                               


                                else:
                                    MyHandler.high = MyHandler.active_player
                                    #set low
                                    if MyHandler.high == MyHandler.p1:
                                        MyHandler.low = MyHandler.p2
                                    else:
                                        MyHandler.low = MyHandler.p1
                             


                            #sides were already selected
                            else:
                                #current player is Low
                                if MyHandler.active_player == MyHandler.low:
                                    #check if low ball was sunk

                                    valid = 0
                                    for ball in sunk_balls:
                                        if ball < 8:
                                            valid = 1
                                    #player sunk their ball
                                    if valid:
                                        print("Valid sink! Go again!")
                                    else:
                                        print("Player sunk opponents ball!")
                                        changeTurn()
                                    
                                #current player is high
                                else:

                                    #check if high ball was sunk
                                    valid = 0
                                    for ball in sunk_balls:
                                        if ball > 8:
                                            valid = 1
                                    #player sunk their ball
                                    if valid:
                                        print("Valid sink! Go again!")
                                    else:
                                        print("Player sunk opponents ball!")
                                        changeTurn()

                        else: #only sunk white ball
                            print("Player only sunk the cue ball!")
                            changeTurn()

                #if no balls are sunk
                if not sunk_balls:
                    #switch current player
                    print("no balls sunk!")
                    changeTurn()
                
                #cue ball and black were not sunk but coloured was
                else:
                    if not MyHandler.low:
                        if sunk_balls[0] < 8:
                            MyHandler.low = MyHandler.active_player

                            #set high
                            if MyHandler.low == MyHandler.p1:
                                MyHandler.high = MyHandler.p2
                            else:
                                MyHandler.high = MyHandler.p1
                    
                        else:
                            MyHandler.high = MyHandler.active_player
                            #set low
                            if MyHandler.high == MyHandler.p1:
                                MyHandler.low = MyHandler.p2
                            else:
                                MyHandler.low = MyHandler.p1
                      
                         
                    #check if correct ball sunk

                    #current player is low
                    if MyHandler.low == MyHandler.active_player:
                        go_again = 0
                        for i in sunk_balls:
                            if i < 8 and i != 0:
                                print(f"{MyHandler.active_player} sunk their ball! Go again")
                                #award a new turn
                                go_again = 1
                        if not go_again:  #if player sinks only opponenets ball
                            print(f"{MyHandler.active_player} sunk only an opponent ball")
                            changeTurn()

                    #current player is high
                    elif MyHandler.high == MyHandler.active_player:
                        go_again = 0
                        for i in sunk_balls:
                            if i > 8 and i != 0:
                                print(f"{MyHandler.active_player} sunk their ball!")
                                #award a new turn
                                go_again = 1
                        if not go_again:  #if player sinks only opponenets ball
                            print(f"{MyHandler.active_player} sunk only an opponent ball")
                            changeTurn()

            #print(MyHandler.table)
                                
            print("Current player: ", MyHandler.active_player)



        

            cur.close()
            conn.close()

                
            #new_player = f"<h1>{MyHandler.active_player}</h1>"
            #content = new_player

            content = str(final_time - MyHandler.start_time)
            



            #print("Done")
            self.send_response(200)  # OK
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(content))
            self.end_headers()  
            self.wfile.write( bytes( content, "utf-8" ) )
     
        
        elif self.path == "/svg.html":
            #print("TABLE???")

            folder_path = os.getcwd()

            # Call the function to delete SVG files
            delete_svg_files(folder_path)

            form = cgi.FieldStorage( fp=self.rfile,
                                     headers=self.headers,
                                     environ = { 'REQUEST_METHOD': 'POST',
                                                 'CONTENT_TYPE': 
                                                   self.headers['Content-Type'],
                                               } 
                                    )

            req_time = form.getvalue('timer')
            #print("JS timer: ", req_time)

            #check database if table with time exists
            db = Physics.Database()

            #get last table time for comparison later
            final_time = db.getLastTime()
           

            #print("Req_time + start_time = ", float(req_time), MyHandler.start_time, (float(req_time) + MyHandler.start_time))

            string_req_time = str(float(req_time) + MyHandler.start_time)

            time = db.checkTableTime(string_req_time)
            
            if time:
                retrieved_table = time + 1 #this is an id
            else:
                retrieved_table = None

            #print("Requested time: ", req_time)


            if retrieved_table:

                
                #print(retrieved_table, " + ", MyHandler.table_id, " = ", retrieved_table + MyHandler.table_id)
                #retrieved_table = retrieved_table + MyHandler.table_id

                #print("Valid time: ", round(float(req_time),2))
                #print(retrieved_table)

                newTable = db.readTable( retrieved_table )
                #print(newTable)

                #get svg of table and send to server
                #print("SERVER: tableid = ", retrieved_table)

                if newTable and retrieved_table:
                    write_svg( retrieved_table, newTable )

                    folder_path = os.getcwd()
                    toSearch = "table%02d.svg" % retrieved_table

                    #print(toSearch)

                    fp = open('./' + toSearch)
                    content = fp.read()
                    self.send_response( 200 ); # OK
                    self.send_header( "Content-type", "text/html" );
                    self.send_header( "Content-length", len( content ) );
                    self.end_headers();

                    self.wfile.write( bytes( content, "utf-8" ) );
                    fp.close();
                    #print("Sent svg")




                else:
                    #print("NULL")
                    last_id = db.getLastTable() - 1

                    #print("Last table? = ", last_id)

                    MyHandler.start_time = db.getLastTime()
                    MyHandler.table_id = last_id #set to last table in shot


                    self.send_response(200)  # OK
                    self.send_header("Content-type", "text/html")
                    self.send_header("Content-length", 0)
                    self.end_headers()  


            else: #segment is done
                #print("cannot get table id")

                if(float(req_time) >= db.getLastTime()):

                    last_id = db.getLastTable() - 1

                    #print("Last table? = ", last_id)

                    MyHandler.start_time = db.getLastTime()
                    MyHandler.table_id = last_id #set to last table in shot


                    self.send_response(200)  # OK
                    self.send_header("Content-type", "text/html")
                    self.send_header("Content-length", 0)
                    self.end_headers()  


                



                if(round(float(req_time),2) >= final_time):
                    #print("This shouldn't be printing")

                    #print("^^ should be the final table")

                    #code
                    html = open( '.'+"/game.html" );
                    html_content = html.read();

                    css = open('.' + "/style.css")
                    css_content = css.read()

                    #get last table in df
                    last_table_id = db.getLastTable()
                    #print("LAST: ", last_table_id)

                            
                    start_table = open('.' + "/table%d.svg" % last_table_id)
                    #tableSvg = start_table.read()
                    tableSvg = start_table.read()

                    jquery = open("." + "/script.js")
                    jquery_content = jquery.read()

                    all_content = f"""
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>8-Ball Pool Game</title>
                        <style>
                            {css_content}
                        </style>
                        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js">
                        </script>
                    </head>
                    <body>
                    <canvas id="canvas"></canvas>
                        <div id='title_container'>
                            <h1 id='p1'>{MyHandler.p1}</h1>
                            <h1 id='p2'>{MyHandler.p2}</h1>
                        </div>
                        <div>
                            <h1 id='curr'>Current turn: {MyHandler.active_player}</h1>
                        </div>
                        <div class="game">
                        
                            <div class="svg_container">                     
                                
                                {tableSvg}
                            </div>
                        </div>
                    
                        <script>
                            {jquery_content}
                        </script>
                    </body>
                    </html>

                    """
                    #print("Sent new page")
                    self.send_response(200)
                    self.send_header( "Content-type", "text/html" )
                    self.send_header( "Content-length", len( all_content ) )
                    self.end_headers()

                    self.wfile.write( bytes( all_content, "utf-8" ) )
                    html.close()
                    css.close()

                self.send_response(200)  # OK
                self.send_header("Content-type", "text/html")
                self.send_header("Content-length", 0)
                self.end_headers()  


                
        elif self.path == "/newturn.html":
            print("A new turn is requested")
            print(MyHandler.active_player)

            stop = 1
            if not stop:
            

                db = Physics.Database()

                #code
                html = open( '.'+"/game.html" );
                html_content = html.read();

                css = open('.' + "/style.css")
                css_content = css.read()

                last_id = db.getLastTable()
                #print("Last id: ", last_id)

                #ensures last table is printed
                write_svg(last_id,MyHandler.table)


                last_table = "/table%d.svg" % (last_id)
                #print(last_table)

                start_table = open('.' + last_table)

                tableSvg = start_table.read()

                jquery = open("." + "/script.js")
                jquery_content = jquery.read()

                all_content = f"""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>8-Ball Pool Game</title>
                    <style>
                        {css_content}
                    </style>
                    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js">
                    </script>
                </head>
                <body>
                <canvas id="canvas"></canvas>
                    <div id='title_container'>
                        <h1 id='p1'>{MyHandler.p1}</h1>
                        <h1 id='p2'>{MyHandler.p2}</h1>
                    </div>
                    <div id='curr_div'>
                        <h1 id='curr'>Current turn: {MyHandler.active_player}</h1>
                    </div>
                    <div class="game">
                    
                        <div class="svg_container">                     
                            
                            {tableSvg}
                        </div>
                    </div>
                
                    <script>
                        {jquery_content}
                    </script>
                </body>
                </html>

                """
            else:

                
                all_content = MyHandler.active_player

                #data = {
                #    "current_player": MyHandler.active_player,
                #    "message": MyHandler.event_message
                #}

                #all_content = json.dumps(data)

            if MyHandler.low: #sides are set
                if MyHandler.low == MyHandler.active_player:
                    all_content = f"{MyHandler.active_player} (Low)"
                    print(MyHandler.active_player, ": Low")
                elif MyHandler.high == MyHandler.active_player:
                    print(MyHandler.active_player, ": High")
                    all_content = f"{MyHandler.active_player} (High)"





            self.send_response(200)
            self.send_header( "Content-type", "text/html" )
            self.send_header( "Content-length", len( all_content ) )
            self.end_headers()

            self.wfile.write( bytes( all_content, "utf-8" ) )
            #html.close()
            #css.close()













          
if __name__ == "__main__":
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler );
    print( "Server listing in port:  ", int(sys.argv[1]) );
    httpd.serve_forever();
    
    

