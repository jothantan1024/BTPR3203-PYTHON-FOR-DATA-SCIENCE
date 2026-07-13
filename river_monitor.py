from datetime import datetime
reading_log = []

river_stations = {
    'Sungai Klang KL': {'state': 'Selangor', 'wqi': 68.3, 'status': ''},
    'Sungai Muar': {'state': 'Johor', 'wqi': 54.1, 'status': ''},
    'Sungai Rajang': {'state': 'Sarawak', 'wqi': 56.3, 'status': ''},
    'Sungai Perlis': {'state': 'Perlis', 'wqi':31.6, 'status': ''}
}

def check_wqi_status(wqi):
    if wqi > 92.7:
        return "Clean"
    elif wqi <= 92.7 and wqi > 76.5:
        return "Slightly Polluted"
    elif wqi <= 76.5 and wqi > 51.9:
        return "Moderately Polluted"
    elif wqi <= 51.9 and wqi > 31.0:
        return "Polluted"
    else:
        return "Heavily Polluted"
    
class RiverStation:
    def __init__(self, name, state, wqi):
        self.name = name
        self.state = state
        self.wqi = wqi
    
    def get_class_label(self):
        return check_wqi_status(self.wqi)
    
    def print_summary(self):
        status = self.get_class_label()
        print(f"{self.name} | {self.state} | WQI: {self.wqi} | {status}")

while True:
    print("\n======== Main Menu ========")
    print("1. Classify All Stations")
    print("2. Add / Update Station")
    print("3. Log Monitoring Reading")
    print("4. Trend Analysis")
    print("5. Export report")
    print("0. Exit")
    
    choice = input("Enter the number based on function: ")

    if choice == '1':
        print("\n--- River Status Report ---")
        for station_name, info in river_stations.items():
            current_wqi = info['wqi']
            calculated_status = check_wqi_status(current_wqi)
            info['status'] = calculated_status
            print(f"{station_name} ({info['state']}) | WQI: {current_wqi} | Status: {info['status']}")
            print("----------------------------")

    elif choice == '2':
        new_name = input("Enter station name: ")
        new_state = input("Enter state: ")
        new_wqi = float(input("Enter WQI value: "))

        if new_name in river_stations:
            river_stations[new_name]['wqi'] = new_wqi
            print(f"Station {new_name} updated with new WQI: {new_wqi}")
        else:
            river_stations[new_name] = {'state': new_state, 'wqi': new_wqi, 'status': ''}
            print(f"New station {new_name} added.")
        for station_name, info in river_stations.items():
            info['status'] = check_wqi_status(info['wqi'])
        print("All stations have been re-classified.")

    elif choice == '3':
        log_name = input("Enter station name to log: ")
        if log_name not in river_stations:
            print(f"Error: Station {log_name} not found.")
        else:
            log_wqi = float(input("Enter new WQI reading (0-100):"))

            if log_wqi < 0 or log_wqi > 100:
                print("Error: WQI value must be between 0 and 100.")
            else:
                current_time = datetime.now()
                reading_log.append((current_time, log_name, log_wqi))
                river_stations[log_name]['wqi'] = log_wqi
                print(f"Station {log_name} updated with new WQI: {log_wqi}")

                for station_name, info in river_stations.items():
                    info['status'] = check_wqi_status(info['wqi'])
                print("All stations have been re-classified.")

                alert_triggered = False
                print("\n--- Alert Check ---")
                for name, info in river_stations.items():
                    if info['wqi'] < 51.9:
                        print(f"[!] ALERT:  {name} in {info['state']} is {info['status']} (WQI:{info['wqi']}).")
                        alert_triggered = True

                if not alert_triggered:
                    print("All monitored rivers are within acceptable quality levels.")
                
                print("\n--- Monitoring Log ---")
                if len(reading_log) == 0:
                    print("No readings have been logged yet.")
                else:
                    for record in reading_log:
                        print(f"Date: {record[0]}, State: {record[1]}, WQI: {record[2]}")

    elif choice == '4':
        print("\n--- Trend Analysis ---")
        print("1. Object-Oriented Station Summaries:")

        station1 = RiverStation("Sungai Klang KL", "Selangor", river_stations["Sungai Klang KL"]["wqi"])
        station1.print_summary()

        station2 = RiverStation("Sungai Muar", "Johor", river_stations["Sungai Muar"]["wqi"])
        station2.print_summary()

        print("\n2. State Average WQI Ranking:")

        state_groups = {}
        for name, info in river_stations.items():
            st = info['state']
            if st not in state_groups:
                state_groups[st] = []
            state_groups[st].append(info['wqi'])
        
        state_averages = []
        for st, wqi_list in state_groups.items():
            avg = sum(wqi_list) / len(wqi_list)
            state_averages.append((avg, st))
        
        state_averages.sort(reverse=True)

        for avg, st in state_averages:
            print(f"{st} | Average WQI: {avg:.2f}")
        
        print("\n3. Station Class Summary Table:")
        class_count = {
            'Clean': 0,
            'Slightly Polluted': 0,
            'Moderately Polluted': 0,
            'Polluted': 0,
            'Heavily Polluted': 0
        }

        for name, info in river_stations.items():
            current_status = info['status']

            if current_status == '':
                current_status = check_wqi_status(info['wqi'])
                info['status'] = current_status
            class_count[current_status] = class_count[current_status] + 1
        
        print(f"{'Class Label':<20} | {'Count'}")
        print("-" * 30)
        for label, count in class_count.items():
            print(f"{label:<20} | {count}")
        
        print("\n4. Greatest Improvement & Decline:")
        station_history = {}

        for record in reading_log:
            log_name = record[1]
            log_wqi = record[2]
            if log_name not in station_history:
               station_history[log_name] = []
            
            station_history[log_name].append(log_wqi)
        
        best_station = ""
        max_improvement = -999.0

        worst_station = ""
        max_decline = 999.0

        valid_data_found = False

        for station, wqi_list in station_history.items():
            if len(wqi_list) >= 2:
                valid_data_found = True
                trend = wqi_list[-1] - wqi_list[0]
                
                if trend > max_improvement:
                    max_improvement = trend
                    best_station = station
                if trend < max_decline:
                    max_decline = trend
                    worst_station = station
        
        if not valid_data_found:
            print("Insufficient data for trend analysis. Please log more readings.")
        else:
            print(f"Greatest Improvement: {best_station} (+{max_improvement:.2f})")
            print(f"Greatest Decline (or least improvement): {worst_station} ({max_decline:.2f})")

    elif choice == '5':
        while True:
            print("\n===== File Menu =====")
            print("1. Export Report")
            print("2. Import Report")
            print("0. Back to Main Menu")

            file_choice = input("Enter your choice: ")

            if file_choice == '1':
                print("\n--- Exporting ---")
                try:
                    with open("river_data.txt", "w") as file:
                        for name, info in river_stations.items():
                            line = f"{name}, {info['state']}, {info['wqi']}, {info['status']}\n"

                            file.write(line)
                        print("Report successfully exported to river_data.txt")
                        break
                
                except PermissionError:
                    print("Error: Permission denied. Cannot write to file.")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
            
            elif file_choice == '2':
                print("\n--- Importing ---")
                try:
                    with open("river_data.txt","r") as file:
                        for line in file:
                            data = line.strip().split(',')

                            name = data[0].strip()
                            state = data[1].strip()
                            wqi = float(data[2].strip())

                            river_stations[name] = {'state': state, 'wqi': wqi, 'status': ''}
                    for station_name, info in river_stations.items():
                        info['status'] = check_wqi_status(info['wqi'])

                    print("Data successfully loaded and re-classified from river_data.txt")
                    break

                except FileNotFoundError:
                    print("Error: The file river_data.txt does not exist.")
                except ValueError:
                    print("Error: The file contains invalid (non-numeric) WQI data")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
            
            elif file_choice == '0':
                print("Return to Main Menu")
                break

            else:
                 print("Invalid input, please try again.")
    elif choice == '0':
        print("Exit System, Good Bye!")
        break
    else:
        print("Invalid input, please input again")