import '@mantine/core/styles.css';
import { MantineProvider, RemoveScroll, Box } from '@mantine/core';

import InputArea from "./InputArea.tsx";
import './App.css';

function App() {
    return (
        <MantineProvider>
            <RemoveScroll>
                <Box sx={{ alignItems: "center"}}>
                    <InputArea />
                </Box>
            </RemoveScroll>
        </MantineProvider>
    );
}

export default App;