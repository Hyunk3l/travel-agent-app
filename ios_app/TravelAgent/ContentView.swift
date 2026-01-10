import SwiftUI

struct ContentView: View {
    @StateObject var viewModel: TravelAgentViewModel

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 24) {
                    hero
                    requestCard
                    responseCard
                }
                .padding(.horizontal, 20)
                .padding(.top, 12)
                .padding(.bottom, 50)
            }
            .scrollIndicators(.hidden)
            .background(background)
            .navigationTitle("Travel Agent")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Text("Local")
                        .font(.caption.weight(.semibold))
                        .padding(.vertical, 6)
                        .padding(.horizontal, 10)
                        .background(Color.orange.opacity(0.18))
                        .cornerRadius(10)
                }
            }
        }
    }

    private var hero: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                VStack(alignment: .leading, spacing: 8) {
                    Text("Plan a local trip")
                        .font(.largeTitle.weight(.bold))
                    Text("Flights + hotels, crafted by your on-device agent.")
                        .foregroundColor(.secondary)
                }
                Spacer()
                HeroBadge()
            }
            HStack(spacing: 12) {
                HeroStat(title: "Latency", value: viewModel.isLoading ? "..." : "Fast")
                HeroStat(title: "Privacy", value: "Local")
                HeroStat(title: "Model", value: "Ollama")
            }
        }
        .padding(24)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(
            RoundedRectangle(cornerRadius: 28)
                .fill(.ultraThinMaterial)
                .overlay(
                    RoundedRectangle(cornerRadius: 28)
                        .stroke(Color.white.opacity(0.2), lineWidth: 1)
                )
        )
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
                        .frame(minHeight: 150)
                        .padding(6)
                        .background(Color.clear)
                }
                .padding(8)
                .background(Color(.systemBackground))
                .overlay(
                    RoundedRectangle(cornerRadius: 16)
                        .stroke(Color.orange.opacity(0.2), lineWidth: 1)
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
        ZStack {
            LinearGradient(
                colors: [Color.orange.opacity(0.25), Color(.systemGroupedBackground)],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            RadialGradient(
                colors: [Color.white.opacity(0.4), Color.clear],
                center: .topTrailing,
                startRadius: 40,
                endRadius: 320
            )
        }
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
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                VStack(alignment: .leading, spacing: 4) {
                    Text("\(flight.carrier) \(flight.flight)")
                        .font(.subheadline.weight(.semibold))
                    Text("Route: \(flight.route)")
                        .foregroundColor(.secondary)
                }
                Spacer()
                PricePill(text: flight.priceString)
            }
            Divider().opacity(0.2)
            HStack {
                TripMeta(label: "Depart", value: flight.depart)
                Spacer()
                TripMeta(label: "Return", value: flight.returnDate)
            }
        }
        .padding(14)
        .background(Color.orange.opacity(0.08))
        .cornerRadius(14)
    }
}

private struct HotelCard: View {
    let hotel: HotelOption

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                VStack(alignment: .leading, spacing: 4) {
                    Text(hotel.name)
                        .font(.subheadline.weight(.semibold))
                    Text(hotel.city)
                        .foregroundColor(.secondary)
                }
                Spacer()
                PricePill(text: hotel.priceString + " / night")
            }
            Divider().opacity(0.2)
            TripMeta(label: "Checkout", value: hotel.checkout)
        }
        .padding(14)
        .background(Color.orange.opacity(0.08))
        .cornerRadius(14)
    }
}

private struct PricePill: View {
    let text: String

    var body: some View {
        Text(text)
            .font(.caption.weight(.semibold))
            .padding(.vertical, 6)
            .padding(.horizontal, 10)
            .background(Color.orange.opacity(0.2))
            .cornerRadius(999)
    }
}

private struct TripMeta: View {
    let label: String
    let value: String

    var body: some View {
        VStack(alignment: .leading, spacing: 2) {
            Text(label)
                .font(.caption)
                .foregroundColor(.secondary)
            Text(value)
                .font(.subheadline)
        }
    }
}

private struct HeroBadge: View {
    var body: some View {
        VStack(spacing: 6) {
            Image(systemName: "sparkles")
                .font(.title3)
            Text("AI")
                .font(.caption.weight(.bold))
        }
        .padding(10)
        .background(Color.orange.opacity(0.2))
        .clipShape(Circle())
    }
}

private struct HeroStat: View {
    let title: String
    let value: String

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(title)
                .font(.caption)
                .foregroundColor(.secondary)
            Text(value)
                .font(.subheadline.weight(.semibold))
        }
        .padding(10)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Color.white.opacity(0.35))
        .cornerRadius(14)
    }
}
