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
    @Published var inlineStatus: String = "Thinking…"
    @Published var showInlineStatus: Bool = false

    private let client: ApiClient
    private var nodeStates: [String: NodeStatus] = [
        "orchestrator": NodeStatus(state: .idle, label: "idle"),
        "flight_search": NodeStatus(state: .idle, label: "idle"),
        "hotel_search": NodeStatus(state: .idle, label: "idle"),
    ]

    init(client: ApiClient = ApiClient()) {
        self.client = client
    }

    func nodeStatus(for id: String) -> NodeStatus {
        nodeStates[id] ?? NodeStatus(state: .idle, label: "idle")
    }

    func send() {
        guard !message.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty else {
            return
        }

        isLoading = true
        showInlineStatus = true
        inlineStatus = "Thinking…"
        answer = ""
        queryLine = ""
        flights = []
        hotels = []
        setNodeState("orchestrator", state: .running, label: "routing")
        setNodeState("flight_search", state: .running, label: "queued")
        setNodeState("hotel_search", state: .running, label: "queued")

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
                setNodeState("orchestrator", state: .done, label: "done")
                if flights.isEmpty {
                    setNodeState("flight_search", state: .skipped, label: "skipped")
                } else {
                    setNodeState("flight_search", state: .done, label: "done")
                }
                if hotels.isEmpty {
                    setNodeState("hotel_search", state: .skipped, label: "skipped")
                } else {
                    setNodeState("hotel_search", state: .done, label: "done")
                }
            } catch {
                let elapsed = Date().timeIntervalSince(start)
                statusLine = "Error: \(error.localizedDescription) | Time: \(String(format: "%.1f", elapsed)) s"
                inlineStatus = "There was an error. Please try again."
                showInlineStatus = true
                setNodeState("orchestrator", state: .error, label: "error")
                setNodeState("flight_search", state: .error, label: "error")
                setNodeState("hotel_search", state: .error, label: "error")
            }
            isLoading = false
        }
    }

    private func setNodeState(_ id: String, state: NodeState, label: String) {
        nodeStates[id] = NodeStatus(state: state, label: label)
        objectWillChange.send()
    }
}
