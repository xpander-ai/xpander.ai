"""
Copyright (c) 2025 Xpander, Inc. All rights reserved.
"""

import os
import httpx

def read_file(file_path: str) -> str:
    """
    Read a file from the sandbox.

    Args:
        file_path (str): Path to the file to read.

    Returns:
        str: File content.
    """
    try: 
        if not os.path.exists(file_path):
            return {
                "success": False,
                "message": f"File not found: {file_path}",
                "filepath": file_path,
                "content": ""
            }

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return {
            "success": True,
            "message": "File read successfully",
            "filepath": file_path,
            "content": content
        }
    except Exception as e:
        return f"Error reading file: {str(e)}"

def download_url_to_file(url: str, file_path: str) -> dict:
    """
    Download content from a URL and save it to a file.

    Args:
        url (str): URL to download content from.
        file_path (str): Path where the file should be saved.

    Returns:
        dict: Result of the operation with status information.
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        
        # Download the content with increased timeout and follow_redirects enabled
        with httpx.Client(timeout=60.0, follow_redirects=True) as client:
            # Make an initial HEAD request to check for redirects
            head_response = client.head(url, follow_redirects=True)
            
            # Get the final URL after potential redirects
            final_url = head_response.url
            
            # Now make the actual GET request to the final URL
            response = client.get(str(final_url))
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
            
            # Write content to file
            with open(file_path, 'wb') as f:
                f.write(response.content)
                
        return {
            "success": True,
            "message": "File downloaded and saved successfully",
            "url": url,
            "final_url": str(final_url),
            "filepath": file_path
        }
    except httpx.RequestError as e:
        return {
            "success": False,
            "message": f"Error requesting URL: {str(e)}",
            "url": url,
            "filepath": file_path
        }
    except httpx.HTTPStatusError as e:
        return {
            "success": False,
            "message": f"HTTP error: {e.response.status_code} - {e.response.reason_phrase}",
            "url": url,
            "filepath": file_path,
            "final_url": str(e.response.url) if hasattr(e.response, 'url') else None
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error downloading/saving file: {str(e)}",
            "url": url,
            "filepath": file_path
        }


local_tools = [
    {
        "declaration": {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": "Read a file from the sandbox",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to the file to read"
                        }
                    },
                    "required": ["file_path"]
                },
                "returns": {
                    "type": "object",
                    "properties": {
                        "success": {
                            "type": "boolean",
                            "description": "Whether the file was read successfully"
                        },
                        "message": {
                            "type": "string",
                            "description": "Status message about the operation"
                        },
                        "filepath": {
                            "type": "string",
                            "description": "Path of the file that was read"
                        },
                        "content": {
                            "type": "string",
                            "description": "Content of the file if successful, empty string if not"
                        }
                    },
                    "required": ["success", "message", "filepath", "content"]
                }
            }
        },
        "fn": read_file
    },
    {
        "declaration": {
            "type": "function",
            "function": {
                "name": "download_url_to_file",
                "description": "Download content from a URL and save it to a file",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "URL to download content from"
                        },
                        "file_path": {
                            "type": "string",
                            "description": "Path where the file should be saved"
                        }
                    },
                    "required": ["url", "file_path"]
                },
                "returns": {
                    "type": "object",
                    "properties": {
                        "success": {
                            "type": "boolean",
                            "description": "Whether the file was downloaded and saved successfully"
                        },
                        "message": {
                            "type": "string",
                            "description": "Status message about the operation"
                        },
                        "url": {
                            "type": "string",
                            "description": "URL that was requested"
                        },
                        "final_url": {
                            "type": "string",
                            "description": "Final URL after redirects"
                        },
                        "filepath": {
                            "type": "string",
                            "description": "Path where the file was saved"
                        }
                    },
                    "required": ["success", "message", "url", "final_url", "filepath"]
                }
            }
        },
        "fn": download_url_to_file
    }
]

## Helper functions to get the list of tools and the tool by name
local_tools_list = [tool['declaration'] for tool in local_tools]
local_tools_by_name = {tool['declaration']['function']['name']: tool['fn'] for tool in local_tools}