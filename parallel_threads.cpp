
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <cmath>
#include <filesystem>
#include <thread>
#include <mutex>
#include <chrono>

namespace fs = std::filesystem;
std::mutex result_mutex;

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

void worker(const std::vector<std::string> &files, std::vector<Result> &results, int start, int end) {
    std::vector<Result> local_results;
    for (int i = start; i < end; ++i) {
        local_results.push_back(analyze_file(files[i]));
    }
    std::lock_guard<std::mutex> lock(result_mutex);
    results.insert(results.end(), local_results.begin(), local_results.end());
}

int main() {
    std::string input_dir = "data";
    std::vector<std::string> files;
    for (const auto &entry : fs::directory_iterator(input_dir)) {
        if (entry.path().extension() == ".csv")
            files.push_back(entry.path().string());
    }

    const int num_threads = std::thread::hardware_concurrency();
    int chunk_size = files.size() / num_threads;
    std::vector<std::thread> threads;
    std::vector<Result> results;

    auto start_time = std::chrono::high_resolution_clock::now();

    for (int i = 0; i < num_threads; ++i) {
        int start = i * chunk_size;
        int end = (i == num_threads - 1) ? files.size() : start + chunk_size;
        threads.emplace_back(worker, std::ref(files), std::ref(results), start, end);
    }

    for (auto &t : threads) {
        if (t.joinable()) t.join();
    }

    auto end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> duration = end_time - start_time;
    std::cout << "[Parallel Threads] Total Execution Time: " << duration.count() << " seconds\n";

    std::ofstream out("parallel_results_threads.csv");
    out << "file,avg_close,max_price,min_price,volatility\n";
    for (const auto &r : results) {
        out << r.file << "," << r.avg_close << "," << r.max_price << "," << r.min_price << "," << r.volatility << "\n";
    }

    return 0;
}
