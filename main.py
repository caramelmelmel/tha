from cinema_booking_system import CinemaBookingSystem
def main():
    print("Please define movie title and seating map in [Title] [Row] [SeatsPerRow] format:")
    while True:
        try:
            user_input = input("> ").rsplit(maxsplit=2)
            if len(user_input) < 3:
                print("Please provide all required information.")
                continue
                
            title = user_input[0]
            rows = int(user_input[1])
            seats_per_row = int(user_input[2])
            cinema = CinemaBookingSystem(title, rows, seats_per_row)
            break
        except ValueError as e:
            print(f"Error: {str(e)}")
            continue

    while True:
        print("\nWelcome to GIC Cinemas")
        print(f"[1] Book tickets for {cinema.movie_title} ({cinema.get_available_seats()} seats available)")
        print("[2] Check bookings")
        print("[3] Exit")
        print("Please enter your selection:")
        
        choice = input("> ").strip()
        
        if choice == "1":
            while True:
                print("\nEnter number of tickets to book, or enter blank to go back to main menu:")
                tickets_input = input("> ").strip()
                
                if not tickets_input:
                    break
                    
                try:
                    num_tickets = int(tickets_input)
                    if num_tickets <= 0:
                        print("Please enter a positive number.")
                        continue
                        
                    if num_tickets > cinema.get_available_seats():
                        print(f"\nSorry, there are only {cinema.get_available_seats()} seats available.")
                        continue
                        
                    booking = cinema.book_tickets(num_tickets)
                    if booking:
                        print(f"\nSuccessfully reserved {num_tickets} {cinema.movie_title} tickets.")
                        print(f"Booking id: {booking.id}")
                        print("Selected seats:")
                        print(cinema.get_seating_map_display(booking.id))
                        
                        while True:
                            print("Enter blank to accept seat selection, or enter new seating position:")
                            position = input("> ").strip()
                            
                            if not position:
                                print(f"\nBooking id: {booking.id} confirmed.")
                                break
                                
                            # Use the same booking ID when changing positions
                            new_booking = cinema.book_tickets(num_tickets, position, booking.id)
                            if new_booking:
                                booking = new_booking
                                print(f"\nBooking id: {booking.id}")
                                print("Selected seats:")
                                print(cinema.get_seating_map_display(booking.id))
                            else:
                                print("Invalid seating position. Please try again.")
                        break
                    else:
                        print("Unable to allocate seats. Please try a different number of tickets.")
                except ValueError:
                    print("Please enter a valid number.")

    # [Rest of the main function remains the same]
        elif choice == "2":
            while True:
                print("\nEnter booking id, or enter blank to go back to main menu:")
                booking_id = input("> ").strip()
                
                if not booking_id:
                    break
                    
                booking = cinema.get_booking(booking_id)
                if booking:
                    print(f"\nBooking id: {booking.id}")
                    print("Selected seats:")
                    print(cinema.get_seating_map_display(booking.id))
                else:
                    print("Booking not found.")
                    
        elif choice == "3":
            print("\nThank you for using GIC Cinemas system. Bye!")
            break
            
        else:
            print("Invalid selection. Please try again.")

main()