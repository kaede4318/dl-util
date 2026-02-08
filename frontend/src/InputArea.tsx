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

    // Function to submit link to backend and download
    const downloadLink = async (values: { link: string }) => {
        try {
            const res = await fetch('http://localhost:8000/api/download', {
                method: 'POST',
                headers: {'Content-Type': 'application/json',},
                body: JSON.stringify({ link: values.link }),
            });

            if (!res.ok) {
                throw new Error(`HTTP error! status: ${res.status}`);
            }
            
            const blob = await res.blob(); // Convert response to Blob (binary file)
            const url = window.URL.createObjectURL(blob); // Create object URL for the Blob

            // Create a temporary <a> element to trigger download
            const a = document.createElement('a');
            a.href = url;

            // Try to get the filename from the response headers
            const disposition = res.headers.get('Content-Disposition');
            let filename = 'video.mp4'; // <<< TODO: change this
            if (disposition && disposition.includes('filename=')) {
                filename = disposition
                .split('filename=')[1]
                .replace(/["']/g, '')
                .trim();
            }
            a.download = filename;

            // Trigger download
            document.body.appendChild(a);
            a.click();
            a.remove();

            // Release the object URL
            window.URL.revokeObjectURL(url);

            setResponse(`Downloaded ${filename} successfully!`);
        } catch (err: any) {
            setResponse('Error: ' + err.message);
        }
    };

    return (
        <>
            <form onSubmit={form.onSubmit(downloadLink)}>
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

                    <Button type="submit" size="lg">
                        <IconDownload size={30} />
                    </Button>
                </Group>
            </form>

            {response && (
                <Text mt="sm" color="blue">
                    {response}
                </Text>
            )}
        </>
    );
}

export default InputArea;