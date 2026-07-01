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

export async function fetchFriendlist() {
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

export async function fetchFriends() {
   try {
    const response  = await fetch('/api/users/me/friends/');
    if (!response.ok) throw new Error('Error');
    const result    = await response.json();
    return {
      friends: result.friends ?? [],
      pending_friend_requests: result.pending_friend_requests ?? []
    };
  }
  catch (error) {
    console.error('Friend request fetching failed: ', error);
    return { friends: [],  pending_friend_requests: [] };
  }
}
