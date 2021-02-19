# obsbot
obsbot repo: will have bot and server code since they go on same host

Setup:
Discord Setup:
    Create discord bot (token will be put in .env file)
    add to discord server
    give permission
    add role for image approver (will be put in .env file)
Clone repo onto host
    Ensure security/traffic rules allow http on port 80
Rename .envlocal to .env and update values:
    TOKEN= discord bot token from earlier goes here
    SERVER_URL= public IP of host bot/server are runnning/listening on
    DATABASE_NAME= what you want your db name to be 
    CHANNEL_ID= the channel you want the bot to listen to
    APPROVAL_EMOJIS= the emojis you want the bot to listen for (pizza is default) (list)
    APPROVER_ROLES= the roles that you want to bot to listen for approval from ('approver' is default) (list)
    CAROUSEL_DELAY= how long you want the images up before they scroll (3000ms/3s is default)
Set up environment
    python3, pip3
    pip install: flask, sqlite3, dotenv, discord packages
    ensure .env file is accurate
Run the bot and the server
    python3 bot.py
    sudo python3 server.py


my brainstorming notes:
- channel where we/users/ravers post pics they take during the event to be shown on stream/video feed 
- a bot/integration listening to that channel
- when an image in that channel gets emojied/verified by staff/admins (people in this channel as an example) the bot picks it up and adds it to the carousel
- overlay/scene uses browser source of the carousel, server handles image transitions/timing

parts
- channel (#image-submissions in obs' discord) - done(tested)
    - any can submit pics - done(tested)
    - admin/specific role can react with emoji done(tested)
    - lock down to only image uploads (no text possible?) - done
- bot (python script on aws host)
    - listens to right channel in right discord - done
    - listens for reactions on image posts - done
    - if specific reaction by specific people, send image to server via rest api - done
    - have command to empty image queue on server via rest api - done
    - have command to toggle browser source - not doing in discord bot, will be obs chat bot
    - commands
        - empty queue !flush - done
- server (flask app on aws host)
    - single html view with image carousel (bootstrap probably) - done
    - maintain image queue - done
    - transition between images - done
    - rest api
        - add image to queue - done
        - remove image from queue - done
        - skip image - done
        - rewind - not doing
        - empty queue - done
