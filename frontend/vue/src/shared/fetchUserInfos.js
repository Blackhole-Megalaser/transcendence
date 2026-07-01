export async function fetchUserInfos() {
  const url = '/api/users/me/';
  try {
    const response  = await fetch(url);
    if (response.status === 401 || response.status === 403)  return { status: 'unauthenticated' };
    if (!response.ok)             throw new Error('error')
    const result  = await response.json();
    return { status: 'ok', data: result };
  }
  catch {
    return { status: 'error' };
  }
}

export async function fetchFriends() {
  try {
    const response  = await fetch('/api/users/me/friendlist');
    if (!response.ok) throw new Error('Error');
    const result    = await response.json();
    return result.friends;
  }
  catch {
    console.error('Friend fetching failed: ', error);
    return [];
  }
}

export async function fetchFriendRequests() {
   try {
    const response  = await fetch('/api/users/me/friends_request');
    if (!response.ok) throw new Error('Error');
    const result    = await response.json();
    return result.pending_friend_requests;
  }
  catch (error) {
    console.error('Friend request fetching failed: ', error);
    return [];
  }
}
