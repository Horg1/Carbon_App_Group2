from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from capp import db
from capp.models import Transport
from datetime import timedelta, datetime
from capp.carbon_app.forms import BusForm, CarForm, BoatForm, PlaneForm, MetroForm, TrainForm, TruckForm

carbon_app = Blueprint('carbon_app', __name__)

efco2_freight = {
    'Truck': {'Diesel': 0.096, 'LNG': 0.080, 'HVO': 0.010, 'Electric': 0.000},
    'Plane': {'Jet Fuel': 0.800, 'SAF': 0.160},
    'Ferry': {'Diesel': 0.016, 'LNG': 0.013, 'Electric': 0.000}
}

efco2={'Bus':{'Diesel':0.10231,'CNG':0.08,'Petrol':0.10231,'No Fossil Fuel':0},
    'Car':{'Petrol':0.18592,'Diesel':0.16453,'No Fossil Fuel':0},
    'Plane':{'Petrol':0.24298},
    'Ferry':{'Diesel':0.11131, 'CNG':0.1131, 'No Fossil Fuel':0},
    'Metro':{'No Fossil Fuel':0.00407},
    'Train':{'Diesel':0.04110, 'No Fossil Fuel':0.00410},
    'Motorbike':{'Petrol':0.09816,'No Fossil Fuel':0},
    'Scooter':{'No Fossil Fuel':0},
    'Bicycle':{'No Fossil Fuel':0},
    'Walk':{'No Fossil Fuel':0},
    'Truck':{'Diesel':0.20000,'No Fossil Fuel':0}}
efch4={'Bus':{'Diesel':2e-5,'CNG':2.5e-3,'Petrol':2e-5,'No Fossil Fuel':0},
    'Car':{'Petrol':3.1e-4,'Diesel':3e-6,'No Fossil Fuel':0},
    'Plane':{'Petrol':1.1e-4},
    'Ferry':{'Diesel':3e-5, 'CNG':3e-5,'No Fossil Fuel':0},
    'Metro':{'No Fossil Fuel':0},
    'Train':{'Diesel':1e-5, 'No Fossil Fuel':0},
    'Motorbike':{'Petrol':2.1e-3,'No Fossil Fuel':0},
    'Scooter':{'No Fossil Fuel':0},
    'Bicycle':{'No Fossil Fuel':0},
    'Walk':{'No Fossil Fuel':0},
    'Truck':{'Diesel':3e-5,'No Fossil Fuel':0}}


@carbon_app.route('/carbon_app')
def carbon_app_home():
    return render_template('carbon_app/carbon_app.html', title='carbon_app')


@carbon_app.route('/carbon_app/new_entry')
def new_entry():
    return render_template('carbon_app/new_entry.html', title='new_entry')


# New-entry form functions - we have one for each transport type
@carbon_app.route('/carbon_app/new_entry_bus', methods=['GET','POST'])
@login_required
def new_entry_bus():
    form = BusForm()
    if form.validate_on_submit():
        kms = form.kms.data
        fuel = form.fuel_type.data
        transport = 'Bus'

        co2 = float(kms) * efco2[transport][fuel]
        ch4 = float(kms) * efch4[transport][fuel]
        total = co2+ch4

        co2 = float("{:.2f}".format(co2))
        ch4 = float("{:.2f}".format(ch4))
        total = float("{:.2f}".format(total))

        emissions = Transport(kms=kms, transport=transport, fuel=fuel, co2=co2, ch4=ch4, total=total, user_id=current_user.id)
        db.session.add(emissions)
        db.session.commit()
        return redirect(url_for('carbon_app.your_data'))
    return render_template('carbon_app/new_entry_bus.html', title='new entry bus', form=form)

@carbon_app.route('/carbon_app/new_entry/car', methods=['GET', 'POST'])
@login_required
def new_entry_car():
    form = CarForm()
    if form.validate_on_submit():
        kms = form.kms.data
        fuel = form.fuel_type.data
        transport = 'Car'

        co2 = float(kms) * efco2[transport][fuel]
        ch4 = float(kms) * efch4[transport][fuel]
        total = co2 + ch4

        co2 = float("{:.2f}".format(co2))
        ch4 = float("{:.2f}".format(ch4))
        total = float("{:.2f}".format(total))

        emissions = Transport(kms=kms, transport=transport, fuel=fuel, co2=co2, ch4=ch4, total=total, user_id=current_user.id)
        db.session.add(emissions)
        db.session.commit()
        return redirect(url_for('carbon_app.your_data'))
    return render_template('carbon_app/new_entry_car.html', title='New Car Entry', form=form)

@carbon_app.route('/carbon_app/new_entry/boat', methods=['GET', 'POST'])
@login_required
def new_entry_boat():
    form = BoatForm()
    if form.validate_on_submit():
        kms = form.kms.data
        fuel = form.fuel_type.data
        seafood_kg = form.seafood_kg.data
        transport = 'Ferry'
        weight_tonnes = seafood_kg / 1000
        total_co2e = float(weight_tonnes) * float(kms) * efco2_freight[transport][fuel]
        total_co2e = float("{:.4f}".format(total_co2e))
        emissions = Transport(kms=kms, transport=transport, fuel=fuel, co2=total_co2e, ch4=0.0, total=total_co2e, seafood_kg=seafood_kg, user_id=current_user.id)
        db.session.add(emissions)
        db.session.commit()
        return redirect(url_for('carbon_app.your_data'))
    return render_template('carbon_app/new_entry_boat.html', title='New Boat Entry', form=form)

@carbon_app.route('/carbon_app/new_entry/plane', methods=['GET', 'POST'])
@login_required
def new_entry_plane():
    form = PlaneForm()
    if form.validate_on_submit():
        kms = form.kms.data
        fuel = form.fuel_type.data
        seafood_kg = form.seafood_kg.data
        transport = 'Plane'
        weight_tonnes = seafood_kg / 1000
        total_co2e = float(weight_tonnes) * float(kms) * efco2_freight[transport][fuel]
        total_co2e = float("{:.4f}".format(total_co2e))
        emissions = Transport(kms=kms, transport=transport, fuel=fuel, co2=total_co2e, ch4=0.0, total=total_co2e, seafood_kg=seafood_kg, user_id=current_user.id)
        db.session.add(emissions)
        db.session.commit()
        return redirect(url_for('carbon_app.your_data'))
    return render_template('carbon_app/new_entry_plane.html', title='New Plane Entry', form=form)

@carbon_app.route('/carbon_app/new_entry/metro', methods=['GET', 'POST'])
@login_required
def new_entry_metro():
    form = MetroForm()
    if form.validate_on_submit():
        kms = form.kms.data
        fuel = form.fuel_type.data
        transport = 'Metro'
        co2 = float(kms) * efco2[transport][fuel]
        ch4 = float(kms) * efch4[transport][fuel]
        total = co2 + ch4
        co2 = float("{:.2f}".format(co2))
        ch4 = float("{:.2f}".format(ch4))
        total = float("{:.2f}".format(total))
        emissions = Transport(kms=kms, transport=transport, fuel=fuel, co2=co2, ch4=ch4, total=total, user_id=current_user.id)
        db.session.add(emissions)
        db.session.commit()
        return redirect(url_for('carbon_app.your_data'))
    return render_template('carbon_app/new_entry_metro.html', title='New Metro Entry', form=form)

@carbon_app.route('/carbon_app/new_entry/truck', methods=['GET', 'POST'])
@login_required
def new_entry_truck():
    form = TruckForm()
    if form.validate_on_submit():
        kms = form.kms.data
        fuel = form.fuel_type.data
        seafood_kg = form.seafood_kg.data
        transport = 'Truck'
        weight_tonnes = seafood_kg / 1000
        total_co2e = float(weight_tonnes) * float(kms) * efco2_freight[transport][fuel]
        total_co2e = float("{:.4f}".format(total_co2e))
        emissions = Transport(kms=kms, transport=transport, fuel=fuel, co2=total_co2e, ch4=0.0, total=total_co2e, seafood_kg=seafood_kg, user_id=current_user.id)
        db.session.add(emissions)
        db.session.commit()
        return redirect(url_for('carbon_app.your_data'))
    return render_template('carbon_app/new_entry_truck.html', title='New Truck Entry', form=form)

@carbon_app.route('/carbon_app/new_entry/train', methods=['GET', 'POST'])
@login_required
def new_entry_train():
    form = TrainForm()
    if form.validate_on_submit():
        kms = form.kms.data
        fuel = form.fuel_type.data
        transport = 'Train'
        co2 = float(kms) * efco2[transport][fuel]
        ch4 = float(kms) * efch4[transport][fuel]
        total = co2 + ch4
        co2 = float("{:.2f}".format(co2))
        ch4 = float("{:.2f}".format(ch4))
        total = float("{:.2f}".format(total))
        emissions = Transport(kms=kms, transport=transport, fuel=fuel, co2=co2, ch4=ch4, total=total, user_id=current_user.id)
        db.session.add(emissions)
        db.session.commit()
        return redirect(url_for('carbon_app.your_data'))
    return render_template('carbon_app/new_entry_train.html', title='New Train Entry', form=form)

# Your data

@carbon_app.route('/carbon_app/your_data')
@login_required
def your_data():
    user_id = current_user.id
    entries = Transport.query.filter_by(user_id=user_id)\
        .filter(Transport.date >= datetime.now() - timedelta(days=30))\
        .order_by(Transport.date.desc()).order_by(Transport.transport.asc()).all()

    emissions_by_transport = db.session.query(db.func.sum(Transport.total), Transport.transport). \
        filter(Transport.date > (datetime.now() - timedelta(days=30))).filter_by(user_id=user_id). \
        group_by(Transport.transport).order_by(Transport.transport.asc()).all()
    emission_transport = [0, 0, 0]
    first_tuple_elements = []
    second_tuple_elements = []
    for a_tuple in emissions_by_transport:
        first_tuple_elements.append(a_tuple[0])
        second_tuple_elements.append(a_tuple[1])

    if 'Truck' in second_tuple_elements:
        index_truck = second_tuple_elements.index('Truck')
        emission_transport[0]=first_tuple_elements[index_truck]

    if 'Plane' in second_tuple_elements:
        index_plane = second_tuple_elements.index('Plane')
        emission_transport[1]=first_tuple_elements[index_plane]

    if 'Ferry' in second_tuple_elements:
        index_ferry = second_tuple_elements.index('Ferry')
        emission_transport[2]=first_tuple_elements[index_ferry]
    # Emissions by date (individual)
    date_col = db.func.date(Transport.date)
    emissions_by_date = db.session.query(db.func.sum(Transport.total), date_col). \
        filter(Transport.date > (datetime.now() - timedelta(days=30))).filter_by(user_id=user_id). \
        group_by(date_col).order_by(date_col.asc()).all()
    over_time_emissions = []
    dates_label = []
    for total, date in emissions_by_date:
        dates_label.append(date if isinstance(date, str) else date.strftime("%d-%m-%Y"))
        over_time_emissions.append(total)

    # CO₂e per kg by transport type (efficiency bar chart)
    efficiency_by_transport_query = db.session.query(
        db.func.sum(Transport.total),
        db.func.sum(Transport.seafood_kg),
        Transport.transport
    ).filter(Transport.date > (datetime.now() - timedelta(days=30))).filter_by(user_id=user_id). \
        group_by(Transport.transport).all()
    efficiency_transport_labels = []
    efficiency_transport_values = []
    for total_co2, total_kg, transport_type in efficiency_by_transport_query:
        if total_kg and total_kg > 0:
            efficiency_transport_labels.append(transport_type)
            efficiency_transport_values.append(round(total_co2 / total_kg, 4))

    # CO₂e per kg over time (efficiency line chart)
    efficiency_by_date_query = db.session.query(
        db.func.sum(Transport.total),
        db.func.sum(Transport.seafood_kg),
        date_col
    ).filter(Transport.date > (datetime.now() - timedelta(days=30))).filter_by(user_id=user_id). \
        group_by(date_col).order_by(date_col.asc()).all()
    over_time_efficiency = []
    for total_co2, total_kg, _ in efficiency_by_date_query:
        if total_kg and total_kg > 0:
            over_time_efficiency.append(round(total_co2 / total_kg, 4))
        else:
            over_time_efficiency.append(None)

    return render_template('carbon_app/your_data.html', title='your_data', entries=entries,
                           emissions_by_transport=emission_transport,
                           over_time_emissions=over_time_emissions,
                           dates_label=dates_label,
                           efficiency_transport_labels=efficiency_transport_labels,
                           efficiency_transport_values=efficiency_transport_values,
                           over_time_efficiency=over_time_efficiency)

@carbon_app.route('/carbon_app/delete_emissions/<int:entry_id>')
def delete_emissions(entry_id):
    entry=Transport.query.get_or_404(int(entry_id))
    db.session.delete(entry)
    db.session.commit()
    flash("Entry deleted", "success")
    return redirect(url_for('carbon_app.your_data'))