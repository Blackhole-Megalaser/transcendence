export async function fetchUserInfos() {
  const url = '/api/users/me/';
  try {
    const response  = await fetch(url);
    if (response.status === 401 || response.status === 403)  return { status: 'unauthenticated' };
    if (!response.ok)             throw new Error('error')
    const result  = await response.json();
    return { status: 'ok', data: result};
  }
  catch {
    return { status: 'error' };
  }
}
