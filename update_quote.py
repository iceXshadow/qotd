import requests
import re
import time

def update_quote(max_retries=3, retry_delay=5):
    for attempt in range(max_retries):
        try:
            # Fetch a random quote from ZenQuotes API
            response = requests.get('https://zenquotes.io/api/random')
            response.raise_for_status()
            data = response.json()
            quote = data[0]['q']
            author = data[0]['a']

            # Update README.md with quote and attribution
            with open('README.md', 'r') as file:
                readme = file.read()
            quote_section_regex = r'<!-- QUOTE_START -->[\s\S]*?<!-- QUOTE_END -->'
            new_quote_section = (
                f'<!-- QUOTE_START -->\n> {quote}\n>\n> — {author}\n\n'
                f'Inspirational quotes provided by <a href="https://zenquotes.io/" target="_blank">ZenQuotes API</a>\n'
                f'<!-- QUOTE_END -->'
            )
            readme = re.sub(quote_section_regex, new_quote_section, readme)
            with open('README.md', 'w') as file:
                file.write(readme)

            # Update quotes.py
            with open('quotes.py', 'r') as file:
                quotes_content = file.read()
            # Find the position to insert the new quote
            insert_pos = quotes_content.find('quotes = [') + len('quotes = [')
            new_quote_line = f'\n    "{quote.replace('"', '\\"')}",'
            updated_content = quotes_content[:insert_pos] + new_quote_line + quotes_content[insert_pos:]
            with open('quotes.py', 'w') as file:
                file.write(updated_content)

            print(f"Successfully updated quote: {quote}")
            return

        except requests.exceptions.RequestException as req_err:
            print(f"Request Error on attempt {attempt + 1}: {req_err}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            continue
        except Exception as e:
            print(f"Unexpected error: {e}")
            exit(1)

    print(f"Failed to update quote after {max_retries} attempts")
    exit(1)

if __name__ == "__main__":
    update_quote()