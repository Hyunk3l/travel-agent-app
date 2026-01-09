import Foundation
import SwiftUI

@MainActor
final class TravelAgentViewModel: ObservableObject {
    @Published var message: String = "SFO to LAX, depart 2025-01-10. Flights only."
    @Published var queryLine: String = "Waiting for a request."
    @Published var answer: String = ""
    @Published var flights: [FlightOption] = []
    @Published var hotels: [HotelOption] = []
    @Published var statusLine: String = "Status: idle | Time: 0.0 s"
    @Published var isLoading: Bool = false
    @Published var inlineStatus: String = "Thinking..."
    @Published var showInlineStatus: Bool = false

    private let client: ApiClient

    init(client: ApiClient = ApiClient()) {
        self.client = client
    }

    func send() {
        guard !message.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty else {
            return
        }

        isLoading = true
        showInlineStatus = true
        inlineStatus = "Thinking..."
        answer = ""
        queryLine = ""
        flights = []
        hotels = []

        let start = Date()

        Task {
            do {
                let response = try await client.chat(message: message)
                let elapsed = Date().timeIntervalSince(start)
                queryLine = response.query.map { "Query: \($0)" } ?? "Query: not available"
                flights = response.flights ?? []
                hotels = response.hotels ?? []

                if flights.isEmpty && hotels.isEmpty {
                    answer = response.answer ?? "No structured results."
                } else {
                    answer = ""
                }

                statusLine = "Status: \(response.status ?? "unknown") | Time: \(String(format: "%.1f", elapsed)) s"
                showInlineStatus = false
            } catch {
                let elapsed = Date().timeIntervalSince(start)
                statusLine = "Error: \(error.localizedDescription) | Time: \(String(format: "%.1f", elapsed)) s"
                inlineStatus = "There was an error. Please try again."
                showInlineStatus = true
            }
            isLoading = false
        }
    }
}
