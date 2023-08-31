import React, {Suspense} from "react"
import defaultTheme from "./themes/defaultTheme";
import {ThemeProvider} from "@mui/material";

import PageLoader from "./components/PageLoader";
import SocketContext, {socket} from "./contexts/socketContext";
import Transcode from "./pages/Transcode";


function App(){
    return (
        <ThemeProvider theme={defaultTheme}>
            <SocketContext.Provider value={socket}>
                <Suspense fallback={<PageLoader />}>
                    <Transcode />
                </Suspense>
            </SocketContext.Provider>
        </ThemeProvider>
    )
}

export default App;
