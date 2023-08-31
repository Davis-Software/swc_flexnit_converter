import {io, Socket} from "socket.io-client"
import {SOCKET_ROUTE} from "../utils/constants";
import React from "react";

const socket: Socket = io(SOCKET_ROUTE, {
    reconnection: true,
    reconnectionDelay: 500,
    reconnectionAttempts: 5,
    upgrade: true,
    transports: ["websocket"],
})
const SocketContext = React.createContext(socket)

socket.on("connect", () => {
    console.log("Connected to socket")
})
socket.on("disconnect", () => {
    console.log("Disconnected from socket")
})

export default SocketContext
export {socket}
