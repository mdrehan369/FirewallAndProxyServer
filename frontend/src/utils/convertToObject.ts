export function convertToObject(
  data: string,
  delimiter: string,
  keyValueDelimiter: string
) {
  const keyValuePair = data.split(delimiter).filter((kv) => kv != "");
  const obj: Record<string, string> = {};
  for (const keyValue of keyValuePair) {
    const key = keyValue.split(keyValueDelimiter)[0];
    const value = keyValue
      .split(keyValueDelimiter)
      .slice(1)
      .join(keyValueDelimiter);
    obj[key] = value;
  }
  return obj;
}
