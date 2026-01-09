import Foundation

final class ApiClient {
    enum ApiError: Error {
        case invalidResponse
    }

    private let baseURL: URL

    init(baseURL: URL = URL(string: "http://127.0.0.1:8000")!) {
        self.baseURL = baseURL
    }

    func chat(message: String) async throws -> ChatResponse {
        var request = URLRequest(url: baseURL.appendingPathComponent("chat"))
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = try JSONEncoder().encode(ChatRequest(message: message))

        let (data, response) = try await URLSession.shared.data(for: request)
        guard let http = response as? HTTPURLResponse, (200...299).contains(http.statusCode) else {
            throw ApiError.invalidResponse
        }
        return try JSONDecoder().decode(ChatResponse.self, from: data)
    }
}
