export default class APIService {
  static async createNote(credentials){
    let response = await fetch('/api/v1/text-blocks/create/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials)
    })
    let data = await response.json();
    return {
      status: response.status,
      hash: data.hash
    };
  }

  static async getNoteDetails(hash) {
    let response = await fetch(`/api/v1/text-blocks/${hash}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    let data = await response.json()

    return data
  }
}