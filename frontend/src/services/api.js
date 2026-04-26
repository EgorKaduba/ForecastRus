const API_BASE_URL = 'http://localhost:8000'



export async function fetchRegions() {
    const response = await fetch(`${API_BASE_URL}/api/v1/regions/`)
    const data = await response.json()
    return data.map(item => item.region_name)
}

export async function fetchLands() {
    const response = await fetch(`${API_BASE_URL}/api/v1/regions/krais`)
    const data = await response.json()
    return data.map(item => item.region_name)
}

export async function fetchArea() {
    const response = await fetch(`${API_BASE_URL}/api/v1/regions/obls`)
    const data = await response.json()
    return data.map(item => item.region_name)
}

export async function fetchRepublic() {
    const response = await fetch(`${API_BASE_URL}/api/v1/regions/republics`)
    const data = await response.json()
    return data.map(item => item.region_name)
}
