import { Button, Group, TextInput, Box, Text } from '@mantine/core';
import { useForm } from '@mantine/form';
import { useState } from 'react';
import { IconDownload } from '@tabler/icons-react';

function InputArea() {
    const [response, setResponse] = useState<string | null>(null);

    const form = useForm({
            mode: 'uncontrolled',
            initialValues: {
            link: '',
        },

        validate: {
            link: (value) => (/^(https?:\/\/)?([\w-]+\.)+[\w-]+(\/[\w- ./?%&=]*)?$/.test(value) ? null : 'Invalid link'),
        },
    });

    // Function to submit link to backend
    const submitLink = async (values: { link: string }) => {
        try {
            const res = await fetch('http://localhost:8000/api/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ link: values.link }),
            });

            const data = await res.json();
            setResponse(JSON.stringify(data));
        } catch (err) {
            setResponse('Error: ' + err);
        }
    };

    return (
        <>
            <form onSubmit={form.onSubmit(submitLink)}>
                <Group justify="flex-end" align="flex-start" mt="md">
                    <Box h={72}>
                        <TextInput
                            w={600}
                            size="lg"
                            placeholder="enter your link here"
                            key={form.key('link')}
                            {...form.getInputProps('link')}
                        />
                    </Box>

                    <Button 
                        type="submit"
                        size="lg"
                    >
                        <IconDownload size={30} />
                    </Button>
                </Group>
            </form>

            {response && (
                <Text mt="sm" color="blue">
                    Response: {response}
                </Text>
            )}
        </>
    );
}

export default InputArea