import React, {Suspense} from "react"
import defaultTheme from "./themes/defaultTheme";
import {ThemeProvider} from "@mui/material";

import PageLoader from "./components/PageLoader";


function App(){
    return (
        <ThemeProvider theme={defaultTheme}>
            <Suspense fallback={<PageLoader />}>
                test
            </Suspense>
        </ThemeProvider>
    )
}

export default App;
