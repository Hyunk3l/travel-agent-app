import SwiftUI

struct ContentView: View {
    @StateObject var viewModel: TravelAgentViewModel

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 20) {
                    requestCard
                    graphCard
                    responseCard
                }
                .padding(.horizontal, 20)
                .padding(.top, 20)
                .padding(.bottom, 40)
            }
            .navigationTitle("Travel Agent")
        }
    }

    private var requestCard: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("Trip request")
                .font(.headline)
            TextEditor(text: $viewModel.message)
                .frame(minHeight: 140)
                .padding(12)
                .background(Color(.systemBackground))
                .overlay(
                    RoundedRectangle(cornerRadius: 12)
                        .stroke(Color.orange.opacity(0.3), lineWidth: 1)
                )
            Button(action: viewModel.send) {
                Text(viewModel.isLoading ? "Working..." : "Ask agent")
                    .frame(maxWidth: .infinity)
            }
            .buttonStyle(.borderedProminent)
            .disabled(viewModel.isLoading)
            HStack(spacing: 8) {
                TagChip(title: "Ollama")
                TagChip(title: "Strands graph")
                TagChip(title: "Local only")
            }
        }
        .padding(20)
        .background(Color.orange.opacity(0.08))
        .cornerRadius(20)
    }

    private var graphCard: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("Live architecture")
                .font(.headline)
            Text("Graph")
                .font(.caption)
                .foregroundColor(.secondary)
                .textCase(.uppercase)
            VStack(spacing: 12) {
                GraphNodeRow(title: "Orchestrator", status: viewModel.nodeStatus(for: "orchestrator"))
                GraphNodeRow(title: "Flight Search", status: viewModel.nodeStatus(for: "flight_search"))
                GraphNodeRow(title: "Hotel Search", status: viewModel.nodeStatus(for: "hotel_search"))
            }
        }
        .padding(20)
        .background(Color(.secondarySystemBackground))
        .cornerRadius(20)
    }

    private var responseCard: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Response")
                .font(.headline)
            Text(viewModel.queryLine)
                .foregroundColor(.secondary)
            if viewModel.showInlineStatus {
                InlineStatusView(text: viewModel.inlineStatus)
            }
            if !viewModel.answer.isEmpty {
                Text(viewModel.answer)
                    .foregroundColor(.primary)
            }
            if !viewModel.flights.isEmpty {
                SectionHeader(title: "Flights")
                ForEach(viewModel.flights) { flight in
                    FlightCard(flight: flight)
                }
            }
            if !viewModel.hotels.isEmpty {
                SectionHeader(title: "Hotels")
                ForEach(viewModel.hotels) { hotel in
                    HotelCard(hotel: hotel)
                }
            }
            Text(viewModel.statusLine)
                .font(.footnote)
                .foregroundColor(.secondary)
        }
        .padding(20)
        .background(Color(.systemBackground))
        .cornerRadius(20)
        .shadow(color: Color.black.opacity(0.05), radius: 10, x: 0, y: 4)
    }
}

private struct TagChip: View {
    let title: String

    var body: some View {
        Text(title)
            .font(.caption)
            .padding(.vertical, 6)
            .padding(.horizontal, 10)
            .background(Color.orange.opacity(0.2))
            .cornerRadius(12)
    }
}

private struct SectionHeader: View {
    let title: String

    var body: some View {
        Text(title)
            .font(.caption)
            .foregroundColor(.secondary)
            .textCase(.uppercase)
            .padding(.top, 8)
    }
}

private struct InlineStatusView: View {
    let text: String

    var body: some View {
        HStack(spacing: 8) {
            Circle()
                .fill(Color.orange)
                .frame(width: 8, height: 8)
            Text(text)
                .font(.subheadline)
        }
        .padding(8)
        .background(Color.orange.opacity(0.15))
        .cornerRadius(12)
    }
}

private struct GraphNodeRow: View {
    let title: String
    let status: NodeStatus

    var body: some View {
        HStack {
            VStack(alignment: .leading, spacing: 4) {
                Text(title)
                    .font(.subheadline)
                Text(status.label)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            Spacer()
            Circle()
                .fill(status.color)
                .frame(width: 12, height: 12)
                .overlay(
                    Circle()
                        .stroke(status.color.opacity(0.3), lineWidth: status.state == .running ? 6 : 0)
                        .animation(.easeInOut(duration: 1.2).repeatForever(), value: status.state)
                )
        }
        .padding(12)
        .background(Color(.systemBackground))
        .cornerRadius(14)
    }
}

private struct FlightCard: View {
    let flight: FlightOption

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            Text("\(flight.carrier) \(flight.flight)")
                .font(.subheadline)
            Text("Route: \(flight.route)")
                .foregroundColor(.secondary)
            Text("Depart: \(flight.depart)")
                .foregroundColor(.secondary)
            Text("Return: \(flight.returnDate)")
                .foregroundColor(.secondary)
            Text("Price: \(flight.priceString)")
                .font(.subheadline)
        }
        .padding(12)
        .background(Color.orange.opacity(0.08))
        .cornerRadius(12)
    }
}

private struct HotelCard: View {
    let hotel: HotelOption

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(hotel.name)
                .font(.subheadline)
            Text("City: \(hotel.city)")
                .foregroundColor(.secondary)
            Text("Checkout: \(hotel.checkout)")
                .foregroundColor(.secondary)
            Text("Price: \(hotel.priceString) / night")
                .font(.subheadline)
        }
        .padding(12)
        .background(Color.orange.opacity(0.08))
        .cornerRadius(12)
    }
}
