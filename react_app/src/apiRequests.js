import apiClient from './apiClient';

export async function getPosts(page = 1) {
  const response = await apiClient.get(`/get_posts?page=${page}`);
  return response.data;
}

export async function likePost(postId) {
  const response = await apiClient.post('/like', { post_id: postId });
  return response.data;
}

export async function unlikePost(postId) {
  const response = await apiClient.post('/unlike', { post_id: postId });
  return response.data;
}

export async function addComment(postId, comment) {
  const response = await apiClient.post('/comment', { post_id: postId, body: comment });
  return response.data;
}

export async function updateComment(postId, commentId, comment) {
  const response = await apiClient.put('/update_comment', { post_id: postId, comment_id: commentId, body: comment });
  return response.data;
}

export async function deleteComment(postId, commentId) {
  const response = await apiClient.delete('/delete_comment', { data: { post_id: postId, comment_id: commentId } });
  return response.data;
}
