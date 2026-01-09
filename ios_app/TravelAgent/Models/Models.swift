import Foundation
import SwiftUI

struct ChatRequest: Encodable {
    let message: String
}

struct ChatResponse: Decodable {
    let answer: String?
    let query: String?
    let flights: [FlightOption]?
    let hotels: [HotelOption]?
    let status: String?
    let execution_time_ms: Double?
}

struct FlightOption: Decodable, Identifiable {
    let id = UUID()
    let carrier: String
    let flight: String
    let route: String
    let depart: String
    let returnDate: String
    let price: Double?
    let priceUSD: Double?
    let currency: String?

    enum CodingKeys: String, CodingKey {
        case carrier
        case flight
        case route
        case depart
        case returnDate = "return"
        case price
        case priceUSD = "price_usd"
        case currency
    }

    var priceString: String {
        let amount = price ?? priceUSD
        let symbol = currency ?? "EUR"
        if let amount {
            return String(format: "%.2f %@", amount, symbol)
        }
        return "—"
    }
}

struct HotelOption: Decodable, Identifiable {
    let id = UUID()
    let name: String
    let city: String
    let checkout: String
    let pricePerNight: Double?
    let priceUSDPerNight: Double?
    let currency: String?

    enum CodingKeys: String, CodingKey {
        case name
        case city
        case checkout
        case pricePerNight = "price_per_night"
        case priceUSDPerNight = "price_usd_per_night"
        case currency
    }

    var priceString: String {
        let amount = pricePerNight ?? priceUSDPerNight
        let symbol = currency ?? "EUR"
        if let amount {
            return String(format: "%.2f %@", amount, symbol)
        }
        return "—"
    }
}

enum NodeState {
    case idle
    case running
    case done
    case skipped
    case error
}

struct NodeStatus {
    let state: NodeState
    let label: String
    var color: Color {
        switch state {
        case .idle:
            return .gray
        case .running:
            return .orange
        case .done:
            return .green
        case .skipped:
            return .gray
        case .error:
            return .red
        }
    }
}
