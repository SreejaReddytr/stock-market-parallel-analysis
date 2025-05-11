
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <cmath>
#include <filesystem>
#include <chrono>
#include <omp.h>

namespace fs = std::filesystem;

struct Result {
    std::string file;
    double avg_close;
    double max_price;
    double min_price;
    double volatility;
};

std::vector<std::string> split(const std::string &line, char delimiter) {
    std::vector<std::string> tokens;
    std::stringstream ss(line);
    std::string item;
    while (getline(ss, item, delimiter)) {
        tokens.push_back(item);
    }
    return tokens;
}

Result analyze_file(const std::string &filepath) {
    std::ifstream file(filepath);
    std::string line;
    std::getline(file, line); // skip header

    std::vector<double> closes, highs, lows;
    while (std::getline(file, line)) {
        auto tokens = split(line, ',');
        if (tokens.size() < 6) continue;
        closes.push_back(std::stod(tokens[4]));
        highs.push_back(std::stod(tokens[2]));
        lows.push_back(std::stod(tokens[3]));
    }

    double sum = 0, max_price = highs[0], min_price = lows[0];
    for (double c : closes) sum += c;
    for (double h : highs) if (h > max_price) max_price = h;
    for (double l : lows) if (l < min_price) min_price = l;

    double mean = sum / closes.size();
    double var = 0;
    for (double c : closes) var += (c - mean) * (c - mean);
    double stddev = std::sqrt(var / closes.size());

    return {fs::path(filepath).filename().string(), mean, max_price, min_price, stddev};
}

int main() {
    std::string input_dir = "data";
    std::vector<std::string> files;
    for (const auto &entry : fs::directory_iterator(input_dir)) {
        if (entry.path().extension() == ".csv")
            files.push_back(entry.path().string());
    }

    std::vector<Result> results(files.size());

    auto start = std::chrono::high_resolution_clock::now();
    #pragma omp parallel for
    for (int i = 0; i < files.size(); ++i) {
        results[i] = analyze_file(files[i]);
    }
    auto end = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double> duration = end - start;
    std::cout << "[OpenMP] Total Execution Time: " << duration.count() << " seconds\n";

    std::ofstream out("parallel_results_openmp.csv");
    out << "file,avg_close,max_price,min_price,volatility\n";
    for (const auto &r : results) {
        out << r.file << "," << r.avg_close << "," << r.max_price << "," << r.min_price << "," << r.volatility << "\n";
    }

    return 0;
}
