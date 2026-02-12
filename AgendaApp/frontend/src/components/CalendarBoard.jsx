import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import listPlugin from '@fullcalendar/list';
import interactionPlugin from '@fullcalendar/interaction';
import jsPDF from 'jspdf';

export default function CalendarBoard({ events }) {
  const calendarEvents = events.map((event) => ({
    id: event.id,
    title: event.title,
    start: `${event.date}T${event.start_time}`,
    end: `${event.date}T${event.end_time}`,
    backgroundColor: event.color,
    borderColor: event.color,
  }));

  const exportPdf = (scope) => {
    const doc = new jsPDF();
    doc.setFontSize(16);
    doc.text(`Smart Agenda - ${scope} view`, 10, 15);
    doc.setFontSize(10);
    events.forEach((event, index) => {
      const line = `${event.date} ${event.start_time}-${event.end_time} | ${event.title} | ${event.category}`;
      doc.text(line, 10, 25 + index * 7);
    });
    doc.save(`agenda-${scope}.pdf`);
  };

  return (
    <div className="card">
      <div className="toolbar">
        <h3>Calendar</h3>
        <div className="grid-3">
          <button onClick={() => exportPdf('day')}>Day PDF</button>
          <button onClick={() => exportPdf('week')}>Week PDF</button>
          <button onClick={() => exportPdf('month')}>Month PDF</button>
        </div>
      </div>
      <FullCalendar
        plugins={[dayGridPlugin, timeGridPlugin, listPlugin, interactionPlugin]}
        initialView="timeGridWeek"
        headerToolbar={{
          left: 'prev,next today',
          center: 'title',
          right: 'timeGridDay,timeGridWeek,dayGridMonth,listWeek',
        }}
        buttonText={{ listWeek: 'Next 7 days' }}
        events={calendarEvents}
        height="auto"
      />
    </div>
  );
}
