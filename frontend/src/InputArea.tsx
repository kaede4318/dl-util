import { Button, Group, TextInput, Text, Loader } from '@mantine/core';
import { useForm } from '@mantine/form';
import { useState } from 'react';
import { IconDownload } from '@tabler/icons-react';

import { API_BASE_URL } from "./config/api";

function InputArea() {
    const [response, setResponse] = useState<string | null>(null);
    const [isDownloading, setIsDownloading] = useState(false); // loading state

    const form = useForm({
        mode: 'uncontrolled',
        initialValues: {
            link: '',
        },
        validate: {
            link: (value) => (/^(https?:\/\/)?([\w-]+\.)+[\w-]+(\/[\w- ./?%&=]*)?$/.test(value) ? null : 'Invalid link'),
        },
    });

    const downloadLink = async (values: { link: string }) => {
        setIsDownloading(true);  // start loading
        setResponse(null);       // reset previous message

        try {
            const res = await fetch(`${API_BASE_URL}/api/download`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ link: values.link }),
            });

            if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

            const blob = await res.blob(); // convert response to Blob (binary file)
            const url = window.URL.createObjectURL(blob); // create object URL for the Blo

            // Create a temporary <a> element to trigger download
            const a = document.createElement('a');
            a.href = url;

            // Try to get the filename from the response headers
            const disposition = res.headers.get('Content-Disposition');
            let filename = 'video.mp4'; // <<< TODO: change this
            if (disposition && disposition.includes('filename=')) {
                filename = disposition.split('filename=')[1].replace(/["']/g, '').trim();
            }
            a.download = filename;

            document.body.appendChild(a); // trigger download
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url); // release obj URL

            setResponse(`Downloaded ${filename} successfully!`);
        } catch (err: any) {
            setResponse('Error: ' + err.message);
        } finally {
            setIsDownloading(false); // Stop loading
        }
    };

    return (
        <>
            <form onSubmit={form.onSubmit(downloadLink)}>
                <Group justify="center" align="flex-start" mt="md">
                    <TextInput
                        size="md"
                        placeholder="enter your link here"
                        key={form.key('link')}
                        {...form.getInputProps('link')}
                        sx={{ flex: 1, minWidth: 0 }}
                        w="60vw"
                        disabled={isDownloading} // disable input while downloading
                    />

                    <Button type="submit" size="md" disabled={isDownloading}>
                        {isDownloading ? <Loader size="sm" /> : <IconDownload size={30} />}
                    </Button>
                </Group>
            </form>

            {isDownloading && (
                <Text mt="sm" color="orange">
                    Downloading... please wait.
                </Text>
            )}

            {response && (
                <Text mt="sm" color={response.startsWith('Error') ? 'red' : 'blue'}>
                    {response}
                </Text>
            )}
        </>
    );
}

export default InputArea;