import SwiftUI

struct ContentView: View {
    @StateObject var viewModel: TravelAgentViewModel

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 24) {
                    header
                    requestCard
                    responseCard
                }
                .padding(.horizontal, 20)
                .padding(.top, 12)
                .padding(.bottom, 40)
            }
            .scrollIndicators(.hidden)
            .background(background)
            .navigationTitle("Travel Agent")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Text("Local")
                        .font(.caption)
                        .padding(.vertical, 6)
                        .padding(.horizontal, 10)
                        .background(Color.orange.opacity(0.15))
                        .cornerRadius(10)
                }
            }
        }
    }

    private var header: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("Plan a local trip")
                .font(.title.bold())
            Text("Ask the agent for flights and hotels. Everything stays on your machine.")
                .foregroundColor(.secondary)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
    }

    private var requestCard: some View {
        CardContainer {
            VStack(alignment: .leading, spacing: 16) {
                Text("Trip request")
                    .font(.headline)
                ZStack(alignment: .topLeading) {
                    if viewModel.message.isEmpty {
                        Text("Describe your trip...")
                            .foregroundColor(.secondary)
                            .padding(.top, 12)
                            .padding(.leading, 6)
                    }
                    TextEditor(text: $viewModel.message)
                        .frame(minHeight: 140)
                        .padding(6)
                        .background(Color.clear)
                }
                .padding(8)
                .background(Color(.systemBackground))
                .overlay(
                    RoundedRectangle(cornerRadius: 14)
                        .stroke(Color.orange.opacity(0.25), lineWidth: 1)
                )

                Button(action: viewModel.send) {
                    HStack {
                        if viewModel.isLoading {
                            ProgressView()
                                .tint(.white)
                        }
                        Text(viewModel.isLoading ? "Working..." : "Ask agent")
                            .fontWeight(.semibold)
                    }
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
        }
    }

    private var responseCard: some View {
        CardContainer {
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
        }
    }

    private var background: some View {
        LinearGradient(
            colors: [Color.orange.opacity(0.2), Color(.systemGroupedBackground)],
            startPoint: .topLeading,
            endPoint: .bottomTrailing
        )
        .ignoresSafeArea()
    }
}

private struct CardContainer<Content: View>: View {
    @ViewBuilder let content: Content

    var body: some View {
        content
            .padding(20)
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(.ultraThinMaterial)
            .cornerRadius(24)
            .overlay(
                RoundedRectangle(cornerRadius: 24)
                    .stroke(Color.white.opacity(0.2), lineWidth: 1)
            )
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
            .padding(.top, 4)
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
        .padding(10)
        .background(Color.orange.opacity(0.15))
        .cornerRadius(12)
    }
}

private struct FlightCard: View {
    let flight: FlightOption

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            Text("\(flight.carrier) \(flight.flight)")
                .font(.subheadline.weight(.semibold))
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
                .font(.subheadline.weight(.semibold))
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
