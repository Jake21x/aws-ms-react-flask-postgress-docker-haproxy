import axios from 'axios';

export default async function fetcher(url, token) {
  return axios
    .get(url, { headers: { Authorization: token } })
    .then((res) => res.data);
}
