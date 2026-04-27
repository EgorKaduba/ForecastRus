const API_BASE_URL = 'http://localhost:8000/api/v1'

export async function fetchRegions() {
    const response = await fetch(`${API_BASE_URL}/regions/`)
    const data = await response.json()
    return data.map(item => item.region_name)
}

export async function fetchLands() {
    const response = await fetch(`${API_BASE_URL}/regions/krais`)
    const data = await response.json()
    return data.map(item => item.region_name)
}

export async function fetchArea() {
    const response = await fetch(`${API_BASE_URL}/regions/obls`)
    const data = await response.json()
    return data.map(item => item.region_name)
}

export async function fetchRepublic() {
    const response = await fetch(`${API_BASE_URL}/regions/republics`)
    const data = await response.json()
    return data.map(item => item.region_name)
}

export async function fetchFederalCity() {
    const response = await fetch(`${API_BASE_URL}/regions/federal_city`)
    const data = await response.json()
    return data.map(item => item.region_name)
}

export const fetchRegionColors = async (year) => {
    const response = await fetch(`${API_BASE_URL}/heatmap/?year_from=${year}`)
    if (!response.ok) {
        throw new Error('Ошибка загрузки цветов')
    }
    return await response.json()
}

export const searchSubject = async (query, year) => {
    try {
        // Шаг 1: Получаем region_id по названию региона
        console.log(`Поиск региона по названию: ${query}`)
        const regionResponse = await fetch(
            `${API_BASE_URL}/regions/${encodeURIComponent(query)}`
        )

        if (!regionResponse.ok) {
            if (regionResponse.status === 404) {
                throw new Error(`Субъект "${query}" не найден`)
            }
            throw new Error(`HTTP error! status: ${regionResponse.status}`)
        }

        const region = await regionResponse.json()
        console.log('Найден регион:', region)

        const regionId = region.region_id || region.id
        if (!regionId) {
            throw new Error(`Не удалось получить ID региона для "${query}"`)
        }

        // Шаг 2: Получаем данные региона за указанный год
        console.log(`Получение данных для region_id=${regionId}, year=${year}`)
        const dataResponse = await fetch(
            `${API_BASE_URL}/regions/${regionId}/${year}`
        )

        if (!dataResponse.ok) {
            if (dataResponse.status === 404) {
                throw new Error(`Данные для "${query}" за ${year} год не найдены`)
            }
            throw new Error(`HTTP error! status: ${dataResponse.status}`)
        }

        const data = await dataResponse.json()
        console.log('Получены данные:', data)

        return data

    } catch (error) {
        console.error('API Error:', error)
        throw error
    }
}