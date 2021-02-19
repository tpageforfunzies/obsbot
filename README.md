# obsbot
obsbot repo: will have bot and server code since they go on same host

my brainstorming notes:
- channel where we/users/ravers post pics they take during the event to be shown on stream/video feed 
- a bot/integration listening to that channel
- when an image in that channel gets emojied/verified by staff/admins (people in this channel as an example) the bot picks it up and adds it to the carousel
- overlay/scene uses browser source of the carousel, server handles image transitions/timing

decisions/questions
 - control carousel source via discord bot or twitch channel chat? (both possible)
 - keep images in memory vs save to server/bucket (cheaper/smaller queue vs $$/bigger queue/persistence)

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
