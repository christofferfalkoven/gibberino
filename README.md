# Gibberish
Messaging app

Daniel Degirmen
Kevin Alemi
Alfred Lindholm
Christoffer Falkovén

1. Description:
The project will focus on creating a messenger (chat room) where users can communicate with
each other. The system will have a centralized part which is responsible for connecting users to
each other, forming a peer-2-peer network. It also keeps track of the message log. As such if the
central server crashes, the connected users can still communicate with each other. Each user will
function as both a server and a client. Users will interact with the program through a GUI, where
they are able to type in messages which will then show up for all users in the room. For
implementation of the program, Python will be the choice of language.

2. Purpose:
The purpose of the project is to create a distributed system, which uses the peer-2-peer
architecture to provide a reliable communication channel. The program will be designed with
fault tolerance, real time updates and a shared state in mind. Since chat rooms are used for real
time communication, the focus will be on real time updates, and creating a peer-2-peer network.

3. Problems which might occur:
Reliability, we want a reliable messaging app that can deliver end to end communication
between two or more users. But we also want centralised storage for the conversations so you
can access conversation history from any device. So if a user switches device they want to be
able to see their previous chatlogs without being forced to use the same device.
What happens if our main server goes out? We need a safe way to store data so if our main
server goes out the users will still have access to their previous conversations. So some sort of
error handling so the user knows if they have disconnected. For this an SQL-database might be
used.
A user crashing should not cause the whole system to go down. Instead the user can re-connect
to the server without having affected other users or the server. If a user crashes, the other nodes
in the system will take over the work.

4. Testing:
Tests will be written which tests the backend of the program, and makes sure that the core of the
program works as intended. These tests will be unit tests made using PyUnit.

5. Demonstration:
We will have some users join the chat room and send messages. We will then discuss what is
going on in the background and how everything is managed.