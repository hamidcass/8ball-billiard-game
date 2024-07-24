$(document).ready(

    function(){

        //console.log("Start js")

        //get player 1 and player 2, current player
        var p1 = $("#p1");
        var p2 = $("#p2");
        var current_player = $("#curr");

        //get cue ball
        circles = $("circle")
        for(var i=0; i<circles.length; i++){
            if (circles[i].getAttribute("fill") == "WHITE"){
                var cue_ball = $(circles[i])
            }
        }

        cue_ball.css("cursor", "pointer");


        //wait for current player to shoot
        //user presses on cue ball

        trackShot = function(){


            var offset = $(this).offset();

            //this is top left of ball: change to center
            
            var x_pos = offset.left - 5;
            
            //var y_pos = offset.top;
            var y_pos = offset.top + 5;

            // var coord = $(this).getBoundingClientRect()
            // var x_pos = (coord.left + coord.right) / 2
            // var y_pos = (coord.top + coord.bottom) / 2

            var current_x_pos, current_y_pos;
            var delta_x_pos, delta_y_pos;

            //define functions for listeners
            dragHandler = function() {
                current_x_pos = event.pageX;
                current_y_pos = event.pageY;
                delta_x_pos = current_x_pos - x_pos;
                delta_y_pos = current_y_pos - y_pos;

                const canvas = $("#canvas")[0];

                canvas.width = document.body.offsetWidth;
                canvas.height = document.body.offsetHeight;

                const ctx = canvas.getContext("2d");

                //draw line from cursor to ball
                ctx.beginPath();
                ctx.moveTo(x_pos, y_pos);
                ctx.lineTo(current_x_pos, current_y_pos);
                ctx.strokeStyle = "WHITE";
                ctx.lineWidth = 5;
                ctx.stroke();

            }

            //triggers when shot is made
            cancelDrag = function() {

                //remove listeners
                $(document).off("mousemove", dragHandler);
                $(document).off("mouseup", cancelDrag);

                const canvas = $("#canvas")[0];

                canvas.width = document.body.offsetWidth;
                canvas.height = document.body.offsetHeight;

                const ctx = canvas.getContext("2d");

                ctx.clearRect(0, 0, canvas.width, canvas.height);
        
                x_vel = -(delta_x_pos * 6);
                y_vel = -(delta_y_pos * 6);
        
                //TODO: CURRENT CAP ON VEL IS 1000, CHANGE THIS TO REQUIRED
        
        
                if (delta_x_pos >= 250){
                    x_vel = -1200;
                }
                if (delta_x_pos <= -250){
                    x_vel = 1200;
                }     
                if (delta_y_pos >= 250){
                    y_vel = -1200;
                }       
                if (delta_y_pos <= -250){
                    y_vel = 1200;
                }

                var done = 0;
    
          
                console.log(x_vel,y_vel,current_player.textContent)

                //sending velocity to shoot ball
                $.ajax({
                    type: "POST",
                    url: "shot.html",
                    data: { 
                        y_vel: y_vel, 
                        x_vel: x_vel,
                        current_player: current_player.textContent
                    },
                    success: function(data){
                        //get svgs
                        done = 1;
                        //console.log("CHECK-----")
                        //console.log(parseFloat(data))

                        

                        //$("#curr").html("<h1>Current turn: </h1>" + data)

                        //retrieve svgs
                        let timer = 0.0;
                        //console.log("Timer = ", timer)

                        function increment(){
                            //console.log(timer)
                            timer += 0.01
                            if (timer < parseFloat(data)){
                                //console.log(timer)

                                //request svg
                                $.ajax({
                                    type: "POST",
                                    url: "svg.html",
                                    data: { 
                                        timer: timer
                                    },
                                    success: function(data){
        
                                        if (!data) {   
                                                 
                                        }else{

                                            

                                            $(".svg_container").html(data);
                                            //console.log("Changed svgs")
        
                                        }
                            
                                        
                                    }
                                    });
                                  



                                setTimeout(increment, 10)
                            }else{
                                //console.log("TImer done")


                                
                                $.ajax({
                                    type: "POST",
                                    url: "newturn.html",
                                    success: function(data){
                                        //console.log(data)

                                        var curr_turn = data
                                 

                                        //display the current player after previous turn
                                        $("#curr").html("Current turn: " + curr_turn)
                                        //$("#message").html(message)
                                        //console.log(message)

                                        console.log("Start listener")

                                        //get cue ball
                                        circles = $("circle")
                                        for(var i=0; i<circles.length; i++){
                                            if (circles[i].getAttribute("fill") == "WHITE"){
                                                var cue_ball = $(circles[i])
                                            }
                                        }

                                        
                                        cue_ball.css("cursor", "pointer");
                                        cue_ball.mousedown(trackShot); 




                                    }
                                })

                            }
                        }

                        increment();
                       
                    }
                })



            }

            //check if mouse is being dragged
            $(document).mousemove(dragHandler);

            //user picks a shot, get velocty and send to server
            $(document).mouseup(cancelDrag);
            //console.log("Line below mouse up listener");

            
        }

        cue_ball.mousedown(trackShot); 
        //console.log("Line Below mouse down listener");  




    }

 
);

