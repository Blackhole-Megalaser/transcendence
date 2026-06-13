export async function getUserInfos() {
  const url = '/api/users/me/';
  try {
    const response  = await fetch(url);
    if (response.status === 401 || response.status === 403)  return null;
    if (!response.ok)             throw new Error('error')
    const result  = await response.json();
    return result;
  }
  catch {
    return null;
  }
}
