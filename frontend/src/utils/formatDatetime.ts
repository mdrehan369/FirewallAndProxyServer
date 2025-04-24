export function formatDateTime(dateInput: string | number | Date): string {
    const date = new Date(dateInput);
    if (isNaN(date.getTime())) return 'Invalid Date';
  
    const options: Intl.DateTimeFormatOptions = {
      year: 'numeric',
      month: 'short',    // e.g., "Apr"
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true       // change to false for 24-hour format
    };
  
    return date.toLocaleString('en-US', options);
  }
  