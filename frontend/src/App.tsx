import '@mantine/core/styles.css';
import { MantineProvider, Button, Text } from '@mantine/core';

import InputArea from "./InputArea.tsx";
import './App.css';

function App() {
  return (
    <MantineProvider>
      <InputArea />
    </MantineProvider>
  );
}

export default App;