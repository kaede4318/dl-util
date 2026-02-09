import { Button, Group, TextInput, Text, Loader } from '@mantine/core';
import { useForm } from '@mantine/form';
import { useState } from 'react';
import { IconDownload } from '@tabler/icons-react';

import { API_BASE_URL } from "./config/api";

// helper function to parse Disposition header
function getFilenameFromDisposition(disposition: string | null) {
    if (!disposition) return null;

    // RFC 5987: filename*
    const filenameStarMatch = disposition.match(/filename\*\s*=\s*([^;]+)/i);
    if (filenameStarMatch) {
        const value = filenameStarMatch[1].trim();

        // expected format: utf-8''<url-encoded>
        const parts = value.split("''", 2);
        if (parts.length === 2) {
            try {
                return decodeURIComponent(parts[1]);
            } catch {
                return parts[1]; // fallback if decoding fails
            }
        }
    }

    // Basic filename
    const filenameMatch = disposition.match(/filename\s*=\s*("?)([^";]+)\1/i);
    if (filenameMatch) {
        return filenameMatch[2];
    }

    return null;
}

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
            const url = window.URL.createObjectURL(blob); // create object URL for the blob

            // Try to get the filename from the response headers
            const disposition = res.headers.get('Content-Disposition');
            const filename = getFilenameFromDisposition(disposition) ?? 'video.mp4'; // fall back on video.mp4

            // Create a temporary <a> element to trigger download
            const a = document.createElement('a');
            a.href = url;
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
                <Group justify="center" align="flex-start" wrap="nowrap" mt="md" maw="700px">
                    <TextInput
                        size="md"
                        placeholder="enter your link here"
                        key={form.key('link')}
                        {...form.getInputProps('link')}
                        sx={{ flex: 1, minWidth: 0 }}
                        w="60vw"
                        disabled={isDownloading} // disable input while downloading
                    />

                    <Button 
                        type="submit" 
                        size="md"
                        loading={isDownloading ? true : undefined} 
                        loaderProps={{ type: 'dots' }}  
                        disabled={isDownloading}
                    >
                        <IconDownload size={"20"} /> {/* how to make the icon scale with button size??? */}
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